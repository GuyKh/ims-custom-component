from __future__ import annotations
import logging
import pytz
import asyncio
from datetime import datetime
from requests.exceptions import ConnectionError as ConnectError, HTTPError, Timeout
from weatheril import *
import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant

from homeassistant.components.weather import (
    PLATFORM_SCHEMA,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_NATIVE_PRECIPITATION,
    WeatherEntity,
)

from homeassistant.const import (
    CONF_MODE,
    CONF_NAME,
    PRESSURE_MBAR,
    SPEED_KILOMETERS_PER_HOUR,
    LENGTH_KILOMETERS,
    LENGTH_MILLIMETERS,
    TEMP_CELSIUS,
)

from .const import (
    ATTRIBUTION,
    ATTR_API_FEELS_LIKE_TEMPERATURE,
    ATTR_API_DEW_POINT,
    ATTR_API_FORECAST_TIME,
    ATTR_API_FORECAST_DATE,
    ATTR_API_HEAT_STRESS,
    ATTR_API_HEAT_STRESS_LEVEL,
    ATTR_API_MAXIMUM_TEMPERATURE,
    ATTR_API_MAXIMUM_UV_INDEX,
    ATTR_API_MINIMUM_TEMPERATURE,
    ATTR_API_RAIN,
    ATTR_API_RELATIVE_HUMIDITY,
    ATTR_API_TEMPERATURE,
    ATTR_API_UV_INDEX,
    ATTR_API_UV_LEVEL,
    ATTR_API_WEATHER_CODE,
    ATTR_API_WIND_BEARING,
    ATTR_API_WIND_CHILL,
    ATTR_API_WIND_SPEED,
    CONF_CITY,
    CONF_MODE,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
    DEFAULT_UPDATE_INTERVAL,
    FORECAST_MODES,
    FORECAST_MODE_HOURLY,
    IMS_PLATFORMS,
    IMS_PLATFORM,
    IMS_PREVPLATFORM,
    ENTRY_WEATHER_COORDINATOR,
    WEATHER_CODE_TO_CONDITION,
    WIND_DIRECTIONS,
)

from homeassistant.const import TEMP_CELSIUS

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CITY): cv.positive_int,
        vol.Required(CONF_LANGUAGE): cv.string,
        vol.Required(CONF_IMAGES_PATH, default="/tmp"): cv.string,
        vol.Optional(
            CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
        ): cv.positive_int,
        vol.Optional(IMS_PLATFORM): cv.string,
        vol.Optional(CONF_MODE, default=FORECAST_MODE_HOURLY): vol.In(FORECAST_MODES),
    }
)


weather = None


from .weather_update_coordinator import WeatherUpdateCoordinator


async def async_setup_platform(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Import the platform into a config entry."""
    _LOGGER.warning(
        "Configuration of IMS Weather (weather entity) in YAML is deprecated "
        "Your existing configuration has been imported into the UI automatically "
        "and can be safely removed from your configuration.yaml file"
    )

    # Add source to config
    config_entry[IMS_PLATFORM] = [IMS_PLATFORMS[1]]

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=config_entry
        )
    )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up IMS Weather entity based on a config entry."""
    domain_data = hass.data[DOMAIN][config_entry.entry_id]
    name = domain_data[CONF_NAME]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]
    city = domain_data[CONF_CITY]
    language = domain_data[CONF_LANGUAGE]
    forecast_mode = domain_data[CONF_MODE]

    unique_id = f"{config_entry.unique_id}"

    # Round Output
    outputRound = "No"

    ims_weather = IMSWeather(
        name, unique_id, forecast_mode, weather_coordinator, city, outputRound
    )

    async_add_entities([ims_weather], False)
    return True


# asda sd asd


class IMSWeather(WeatherEntity):
    """Implementation of an IMSWeather sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_should_poll = False
    _attr_native_precipitation_unit = LENGTH_MILLIMETERS
    _attr_native_pressure_unit = PRESSURE_MBAR
    _attr_native_temperature_unit = TEMP_CELSIUS
    _attr_native_visibility_unit = LENGTH_KILOMETERS
    _attr_native_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR

    def __init__(
        self,
        name: str,
        unique_id,
        forecast_mode: str,
        weather_coordinator: WeatherUpdateCoordinator,
        city: str,
        outputRound: str,
    ) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._weather_coordinator = weather_coordinator
        self._name = name
        self._mode = forecast_mode
        self._unique_id = unique_id
        self._city = city
        self.outputRound = outputRound
        self._ds_data = self._weather_coordinator.data

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def available(self):
        """Return if weather data is available from IMSWeather."""
        return self._weather_coordinator.data is not None

    @property
    def attribution(self):
        """Return the attribution."""
        return self._weather_coordinator.data.current_weather.description

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def native_temperature(self):
        """Return the temperature."""
        temperature = float(self._weather_coordinator.data.current_weather.temperature)

        if self.outputRound == "Yes":
            return round(temperature, 0) + 0
        else:
            return round(temperature, 2)

    @property
    def humidity(self):
        """Return the humidity."""
        humidity = float(self._weather_coordinator.data.current_weather.humidity)

        if self.outputRound == "Yes":
            return round(humidity, 0) + 0
        else:
            return round(humidity, 2)

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        windspeed = float(self._weather_coordinator.data.current_weather.wind_speed)

        if self.outputRound == "Yes":
            return round(windspeed, 0) + 0
        else:
            return round(windspeed, 2)

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return WIND_DIRECTIONS[
            int(self._weather_coordinator.data.current_weather.json["wind_direction_id"])
        ]

    @property
    def condition(self):
        """Return the weather condition."""
        condition = WEATHER_CODE_TO_CONDITION[
            self._weather_coordinator.data.current_weather.json["weather_code"]
        ]
        if not condition or condition == "Nothing":
            condition = WEATHER_CODE_TO_CONDITION[
                self._weather_coordinator.data.forecast.days[0].weather_code
            ]
        return condition

    @property
    def description(self):
        """Return the weather description."""
        description = self._weather_coordinator.data.current_weather.description
        if not description or description == "Nothing":
            description = self._weather_coordinator.data.forecast.days[0].weather
        return description

    @property
    def forecast(self):
        """Return the forecast array."""
        data = None

        if self._mode == "daily":
            data = [
                {
                    ATTR_FORECAST_TIME: entry.date.astimezone(pytz.UTC).isoformat(),
                    ATTR_FORECAST_NATIVE_TEMP: entry.maximum_temperature,
                    ATTR_FORECAST_NATIVE_TEMP_LOW: entry.minimum_temperature,
                    ATTR_FORECAST_CONDITION: WEATHER_CODE_TO_CONDITION[entry.weather_code],
                }
                for entry in self._weather_coordinator.data.forecast.days
            ]
        else:
            data = []
            for entry in self._weather_coordinator.data.forecast.days:
                for hour in entry.hours:
                    data.append(
                        {
                            ATTR_FORECAST_TIME: hour.forecast_time.astimezone(
                                pytz.UTC
                            ).isoformat(),
                            ATTR_FORECAST_NATIVE_TEMP: hour.temperature,
                            ATTR_FORECAST_CONDITION: WEATHER_CODE_TO_CONDITION[hour.weather_code],
                            ATTR_FORECAST_NATIVE_PRECIPITATION: hour.rain,
                            ATTR_FORECAST_WIND_BEARING: WIND_DIRECTIONS[hour.wind_direction_id],
                            ATTR_FORECAST_NATIVE_WIND_SPEED: hour.wind_speed
                            
                        }
                    )
        return data

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self._weather_coordinator.async_add_listener(self.async_write_ha_state)
        )
