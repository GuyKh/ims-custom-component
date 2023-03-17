import json
import logging
import asyncio
from datetime import date
from weatheril import WeatherIL
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from types import SimpleNamespace
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.const import CONF_NAME, TEMP_CELSIUS

from .const import (
    CONFIG_FLOW_VERSION,
    DEFAULT_FORECAST_MODE,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    FORECAST_MODES,
    ENTRY_NAME,
    ENTRY_WEATHER_COORDINATOR,
    PLATFORMS,
    UPDATE_LISTENER,
    CONF_CITY,
    CONF_MODE,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
    FORECAST_MODES,
    FORECAST_MODE_HOURLY,
    FORECAST_MODE_DAILY,
    IMS_PLATFORMS,
    IMS_PLATFORM,
    IMS_PREVPLATFORM,
    ENTRY_WEATHER_COORDINATOR,
    WEATHER_CODE_TO_CONDITION,
    WIND_DIRECTIONS,
)


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


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    _LOGGER.warning(
        "Configuration of IMS Weather sensor in YAML is deprecated "
        "Your existing configuration has been imported into the UI automatically "
        "and can be safely removed from your configuration.yaml file"
    )

    # Define as a sensor platform
    config_entry[IMS_PLATFORM] = [IMS_PLATFORMS[0]]

    # Set as no rounding for compatability
    config_entry[PW_ROUND] = "No"

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
    """Set up IMS Weather sensor entities based on a config entry."""

    domain_data = hass.data[DOMAIN][config_entry.entry_id]

    name = domain_data[CONF_NAME]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]
    city = domain_data[CONF_CITY]
    language = domain_data[CONF_LANGUAGE]
    # units = domain_data[CONF_UNITS]
    forecast_mode = domain_data[CONF_MODE]

    # Add IMS Sensors
    sensors: list[Entity] = []
    sensors.append(ImsCity(hass, city, language, weather_coordinator))
    sensors.append(ImsTemprature(hass, city, language, weather_coordinator))
    sensors.append(ImsRealFeel(hass, city, language, weather_coordinator))
    sensors.append(ImsHumidity(hass, city, language, weather_coordinator))
    sensors.append(ImsWindSpeed(hass, city, language, weather_coordinator))
    sensors.append(ImsRain(hass, city, language, weather_coordinator))
    sensors.append(ImsDateTime(hass, language, weather_coordinator))

    # Add forecast entities
    for daily_forecast in weather_coordinator.data.forecast.days:
        days_delta = (daily_forecast.date.date() - date.today()).days

        sensor_name = ("day" + str(days_delta)) if days_delta > 0 else "today"

        sensors.append(
            IMSForecast(
                hass,
                language,
                weather_coordinator,
                sensor_name,
                daily_forecast,
            )
        )

    async_add_entities(sensors, update_before_add=True)

    return True


class ImsCity(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._city = city
        self._language = language
        self.entity_id = f"sensor.ims_city"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "ישוב"
        else:
            return "City"

    @property
    def state(self):
        return self._weather_coordinator.data.current_weather.location

    @property
    def icon(self):
        return "mdi:city"

    async def async_update(self):
        await self._hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.location


class ImsTemprature(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._language = language
        self.entity_id = f"sensor.ims_temprature"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "טמפרטורה"
        else:
            return "Temprature"

    @property
    def state(self):
        try:
            return self._weather_coordinator.data.current_weather.temperature
        except:
            pass

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def device_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:thermometer"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.temperature


class ImsRealFeel(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._city = city
        self._language = language
        self.entity_id = f"sensor.ims_realfeel"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "מרגיש כמו"
        else:
            return "Real Feel"

    @property
    def state(self):
        try:
            return self._weather_coordinator.data.current_weather.feels_like
        except:
            pass

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    @property
    def icon(self):
        return "mdi:thermometer"

    async def async_update(self):
        await self._hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.feels_like


class ImsHumidity(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._city = city
        self._language = language
        self.entity_id = f"sensor.ims_humidity"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "לחות"
        else:
            return "Humidity"

    @property
    def state(self):
        try:
            return self._weather_coordinator.data.current_weather.humidity
        except:
            pass

    @property
    def unit_of_measurement(self):
        return "%"

    @property
    def icon(self):
        return "mdi:water-percent"

    async def async_update(self):
        await self._hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.humidity


class ImsRain(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._city = city
        self._language = language
        self.entity_id = f"sensor.ims_rain"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "גשם"
        else:
            return "Rain"

    @property
    def state(self):
        try:
            if self._language == "he":
                if self._weather_coordinator.data.current_weather.rain:
                    return "יורד"
                else:
                    return "לא יורד"
            else:
                if self._weather_coordinator.data.current_weather.rain:
                    return "Raining"
                else:
                    return "Not Raining"

        except:
            pass

    @property
    def icon(self):
        return "mdi:weather-rainy"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.wind_speed


class ImsWindSpeed(Entity):
    def __init__(self, hass, city, language, weather_coordinator):
        self._hass = hass
        self._city = city
        self._language = language
        self.entity_id = f"sensor.ims_windspeed"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "מהירות רוח"
        else:
            return "Wind Speed"

    @property
    def state(self):
        try:
            return self._weather_coordinator.data.current_weather.wind_speed
        except:
            pass

    @property
    def unit_of_measurement(self):
        if self._language == "he":
            return 'קמ"ש'
        else:
            return "kph"

    @property
    def icon(self):
        return "mdi:weather-windy"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.wind_speed


class ImsDateTime(Entity):
    def __init__(self, hass, language, weather_coordinator):
        self._hass = hass
        self._language = language
        self.entity_id = f"sensor.ims_forecast_time"
        self._weather_coordinator = weather_coordinator

    @property
    def name(self):
        if self._language == "he":
            return "תאריך"
        else:
            return "Date"

    @property
    def state(self):
        try:
            return self._weather_coordinator.data.current_weather.forecast_time
        except:
            pass

    @property
    def icon(self):
        return "mdi:calendar"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._weather_coordinator.data.current_weather.forecast_time


class IMSForecast(Entity):
    def __init__(self, hass, language, weather_coordinator, sensor_name, forecast):
        self._hass = hass
        self._forecast = forecast
        self._language = language
        self.entity_id = f"sensor.ims_forecast_" + sensor_name
        self._name = sensor_name
        self._weather_coordinator = weather_coordinator
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def state(self):
        return self._forecast.day

    def get_weather_icon(self, weather_code):
        """
        Converts the weather code to ison
        """
        weather = {
            "1250": "mdi:weather-sunny",
            "1220": "mdi:weather-partly-cloudy",
            "1230": "mdi:weather-cloudy",
            "1570": "mdi:weather-dust",
            "1010": "mdi:weather-dust",
            "1160": "mdi:weather-fog",
            "1310": "mdi:weather-sunny-alert",
            "1580": "mdi:weather-sunny-alert",
            "1270": "mdi:weather-fog",
            "1320": "mdi:snowflake-alert",
            "1590": "mdi:snowflake-alert",
            "1300": "mdi:snowflake-melt",
            "1530": "mdi:weather-partly-rainy",
            "1540": "mdi:weather-partly-rainy",
            "1560": "mdi:weather-partly-rainy",
            "1140": "mdi:weather-pourin",
            "1020": "mdi:weather-lightning-rainy",
            "1510": "mdi:weather-lightning",
            "1260": "mdi:weather-windy",
            "1080": "mdi:weather-snowy-rainy",
            "1070": "mdi:weather-snowy-rainy",
            "1060": "mdi:weather-snowy",
            "1520": "mdi:weather-snowy-heavy",
        }
        return weather.get(str(weather_code), "mdi:weather-sunny")

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        attributes = {
            "minimum_temperature": {
                "value": self._forecast.minimum_temperature,
                "unit": TEMP_CELSIUS,
            },
            "maximum_temperature": {
                "value": self._forecast.maximum_temperature,
                "unit": TEMP_CELSIUS,
            },
            "uvi": {"value": self._forecast.maximum_uvi, "unit": "uv"},
            "weather ": {
                "value": self._forecast.weather,
                "icon": self.get_weather_icon(self._forecast.weather_code),
            },
            "description": {"value": self._forecast.description},
            "date": {"value": self._forecast.date.strftime("%Y/%m/%d")},
        }

        for hour in self._forecast.hours:
            attr = {
                "weather": {
                    "value": hour.weather,
                    "icon": self.get_weather_icon(hour.weather_code),
                },
                "temperature": {"value": hour.temperature, "unit": TEMP_CELSIUS},
            }
            attributes[hour.hour] = attr

        self._attributes = attributes
