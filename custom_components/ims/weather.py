from __future__ import annotations
import logging


from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant, callback


from homeassistant.components.weather import (
    # PLATFORM_SCHEMA,
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)

from homeassistant.const import CONF_NAME, UnitOfSpeed, UnitOfPressure, UnitOfLength

from .const import (
    ATTRIBUTION,
    CONF_CITY,
    CONF_MODE,
    DOMAIN,
    FORECAST_MODE_HOURLY,
    IMS_PLATFORMS,
    IMS_PLATFORM,
    ENTRY_WEATHER_COORDINATOR,
    WEATHER_CODE_TO_CONDITION,
    WIND_DIRECTIONS,
)

from homeassistant.const import UnitOfTemperature

from .utils import get_hourly_weather_icon
from .weather_update_coordinator import WeatherUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

weather = None


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
    forecast_mode = domain_data[CONF_MODE]

    is_legacy_city = False
    if isinstance(city, int | str):
        is_legacy_city = True

    unique_id = f"{config_entry.unique_id}"

    # Round Output
    output_round = "No"

    ims_weather = IMSWeather(
        name,
        unique_id,
        forecast_mode,
        weather_coordinator,
        city if is_legacy_city else city["name"],
        output_round,
    )

    async_add_entities([ims_weather], False)


def round_if_needed(value: int | float, output_round: bool):
    if output_round:
        return round(value, 0) + 0
    else:
        return round(value, 2)


class IMSWeather(WeatherEntity):
    """Implementation of an IMSWeather sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_should_poll = False
    _attr_native_precipitation_unit = UnitOfLength.MILLIMETERS
    _attr_native_pressure_unit = UnitOfPressure.MBAR
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_visibility_unit = UnitOfLength.KILOMETERS
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY
    )

    def __init__(
        self,
        name: str,
        unique_id,
        forecast_mode: str,
        weather_coordinator: WeatherUpdateCoordinator,
        city: str,
        output_round: str,
    ) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._weather_coordinator = weather_coordinator
        self._name = name
        self._mode = forecast_mode
        self._unique_id = unique_id
        self._city = city
        self._output_round = output_round == "Yes"
        self._ds_data = self._weather_coordinator.data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()
        assert self.platform.config_entry
        self.platform.config_entry.async_create_task(
            self.hass, self.async_update_listeners(("daily", "hourly"))
        )

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unique_id

    @property
    def available(self):
        """Return if weather data is available from IMSWeather."""
        return (
            self._weather_coordinator.data is not None
            and self._weather_coordinator.data.current_weather is not None
            and self._weather_coordinator.data.forecast is not None
        )

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

        return round_if_needed(temperature, self._output_round)

    @property
    def native_apparent_temperature(self):
        """Return the native apparent temperature (feel-like)."""
        feels_like_temperature = float(
            self._weather_coordinator.data.current_weather.feels_like
        )

        return round_if_needed(feels_like_temperature, self._output_round)

    @property
    def humidity(self):
        """Return the humidity."""
        humidity = float(self._weather_coordinator.data.current_weather.humidity)

        return round_if_needed(humidity, self._output_round)

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        wind_speed = float(self._weather_coordinator.data.current_weather.wind_speed)

        return round_if_needed(wind_speed, self._output_round)

    @property
    def native_dew_point(self):
        """Return the native dew point."""
        dew_point = float(self._weather_coordinator.data.current_weather.due_point_temp)

        return round_if_needed(dew_point, self._output_round)

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return WIND_DIRECTIONS[
            int(self._weather_coordinator.data.current_weather.wind_direction_id)
        ]

    @property
    def uv_index(self):
        """Return the wind bearing."""
        return int(self._weather_coordinator.data.current_weather.u_v_index)

    @property
    def condition(self):
        """Return the weather condition."""

        date_str = self._weather_coordinator.data.current_weather.json["forecast_time"]
        weather_code = get_hourly_weather_icon(
            date_str,
            self._weather_coordinator.data.current_weather.weather_code,
            "%Y-%m-%d %H:%M:%S",
        )

        condition = WEATHER_CODE_TO_CONDITION[str(weather_code)]
        if not condition or condition == "Nothing":
            condition = WEATHER_CODE_TO_CONDITION[
                str(self._weather_coordinator.data.forecast.days[0].weather_code)
            ]
        return condition

    @property
    def description(self):
        """Return the weather description."""
        description = self._weather_coordinator.data.current_weather.description
        if not description or description == "Nothing":
            description = self._weather_coordinator.data.forecast.days[0].weather
        return description

    def _forecast(self, hourly: bool) -> list[Forecast]:
        """Return the forecast array."""
        data: list[Forecast] = []

        if not hourly:
            data = [
                Forecast(
                    condition=WEATHER_CODE_TO_CONDITION[
                        str(daily_forecast.weather_code)
                    ],
                    datetime=daily_forecast.date.isoformat(),
                    native_temperature=daily_forecast.maximum_temperature,
                    native_templow=daily_forecast.minimum_temperature,
                    native_precipitation=sum(
                        hour.rain or 0 for hour in daily_forecast.hours
                    ),
                )
                for daily_forecast in self._weather_coordinator.data.forecast.days
            ]
        else:
            last_weather_code = None
            for daily_forecast in self._weather_coordinator.data.forecast.days:
                for hourly_forecast in daily_forecast.hours:
                    if (
                        hourly_forecast.weather_code
                        and hourly_forecast.weather_code != "0"
                    ):
                        last_weather_code = hourly_forecast.weather_code
                    elif not last_weather_code:
                        last_weather_code = daily_forecast.weather_code

                    hourly_weather_code = get_hourly_weather_icon(
                        hourly_forecast.hour, last_weather_code
                    )

                    data.append(
                        Forecast(
                            condition=WEATHER_CODE_TO_CONDITION[
                                str(hourly_weather_code)
                            ],
                            datetime=hourly_forecast.forecast_time.isoformat(),
                            humidity=hourly_forecast.relative_humidity,
                            native_temperature=hourly_forecast.precise_temperature,
                            native_precipitation=hourly_forecast.rain,
                            precipitation_probability=hourly_forecast.rain_chance,
                            wind_bearing=WIND_DIRECTIONS[
                                hourly_forecast.wind_direction_id
                            ],
                            native_wind_speed=hourly_forecast.wind_speed,
                            uv_index=hourly_forecast.u_v_index,
                        )
                    )

        return data

    @property
    def forecast(self) -> list[Forecast]:
        """Return the forecast array."""
        return self._forecast(hourly=(self._mode == FORECAST_MODE_HOURLY))

    async def async_forecast_daily(self) -> list[Forecast]:
        """Return the daily forecast in native units."""
        return self._forecast(False)

    async def async_forecast_hourly(self) -> list[Forecast]:
        """Return the hourly forecast in native units."""
        return self._forecast(True)

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self._weather_coordinator.async_add_listener(self.async_write_ha_state)
        )
