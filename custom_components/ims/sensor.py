import logging
import types

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import UV_INDEX, UnitOfTemperature, PERCENTAGE, UnitOfSpeed, \
    UnitOfPrecipitationDepth
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from pytz import timezone

from . import ImsEntity, ImsSensorEntityDescription
from .const import (
    DEFAULT_UPDATE_INTERVAL,
    CONF_CITY,
    CONF_MODE,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
    FORECAST_MODES,
    FORECAST_MODE_HOURLY,
    IMS_PLATFORMS,
    IMS_PLATFORM,
    ENTRY_WEATHER_COORDINATOR,
    TYPE_CURRENT_UV_INDEX,
    TYPE_CURRENT_UV_LEVEL,
    TYPE_MAX_UV_INDEX, FIELD_NAME_UV_INDEX, FIELD_NAME_UV_LEVEL, FIELD_NAME_UV_INDEX_MAX, TYPE_HUMIDITY,
    FIELD_NAME_HUMIDITY, FIELD_NAME_TEMPERATURE, FIELD_NAME_LOCATION, TYPE_FEELS_LIKE, FIELD_NAME_FEELS_LIKE,
    FIELD_NAME_RAIN, TYPE_WIND_SPEED, TYPE_FORECAST_TIME, FIELD_NAME_FORECAST_TIME, TYPE_CITY, TYPE_TEMPERATURE,
    FIELD_NAME_WIND_SPEED, TYPE_FORECAST_PREFIX, TYPE_FORECAST_TODAY, TYPE_FORECAST_DAY1, TYPE_FORECAST_DAY2,
    TYPE_FORECAST_DAY3, TYPE_FORECAST_DAY4, TYPE_FORECAST_DAY5, TYPE_FORECAST_DAY6, TYPE_FORECAST_DAY7,
    WEATHER_CODE_TO_ICON, TYPE_PRECIPITATION, TYPE_IS_RAINING, TYPE_PRECIPITATION_PROBABILITY,
    FIELD_NAME_RAIN_CHANCE,
)

IMS_SENSOR_KEY_PREFIX = "ims_"

sensor_keys = types.SimpleNamespace()
sensor_keys.TYPE_CURRENT_UV_INDEX = IMS_SENSOR_KEY_PREFIX + TYPE_CURRENT_UV_INDEX
sensor_keys.TYPE_CURRENT_UV_LEVEL = IMS_SENSOR_KEY_PREFIX + TYPE_CURRENT_UV_LEVEL
sensor_keys.TYPE_MAX_UV_INDEX = IMS_SENSOR_KEY_PREFIX + TYPE_MAX_UV_INDEX
sensor_keys.TYPE_CITY = IMS_SENSOR_KEY_PREFIX + TYPE_CITY
sensor_keys.TYPE_TEMPERATURE = IMS_SENSOR_KEY_PREFIX + TYPE_TEMPERATURE
sensor_keys.TYPE_HUMIDITY = IMS_SENSOR_KEY_PREFIX + TYPE_HUMIDITY
sensor_keys.TYPE_FORECAST_TIME = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_TIME
sensor_keys.TYPE_FEELS_LIKE = IMS_SENSOR_KEY_PREFIX + TYPE_FEELS_LIKE
sensor_keys.TYPE_IS_RAINING = IMS_SENSOR_KEY_PREFIX + TYPE_IS_RAINING
sensor_keys.TYPE_PRECIPITATION = IMS_SENSOR_KEY_PREFIX + TYPE_PRECIPITATION
sensor_keys.TYPE_PRECIPITATION_PROBABILITY = IMS_SENSOR_KEY_PREFIX + TYPE_PRECIPITATION_PROBABILITY
sensor_keys.TYPE_WIND_SPEED = IMS_SENSOR_KEY_PREFIX + TYPE_WIND_SPEED
sensor_keys.TYPE_FORECAST_TODAY = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_TODAY
sensor_keys.TYPE_FORECAST_DAY1 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY1
sensor_keys.TYPE_FORECAST_DAY2 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY2
sensor_keys.TYPE_FORECAST_DAY3 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY3
sensor_keys.TYPE_FORECAST_DAY4 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY4
sensor_keys.TYPE_FORECAST_DAY5 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY5
sensor_keys.TYPE_FORECAST_DAY6 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY6
sensor_keys.TYPE_FORECAST_DAY7 = IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY7

_LOGGER = logging.getLogger(__name__)

UV_LEVEL_EXTREME = "extreme"
UV_LEVEL_VHIGH = "very_high"
UV_LEVEL_HIGH = "high"
UV_LEVEL_MODERATE = "moderate"
UV_LEVEL_LOW = "low"

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

forecast_mode = types.SimpleNamespace()
forecast_mode.CURRENT = "current"
forecast_mode.DAILY = "daily"
forecast_mode.HOURLY = "hourly"


SENSOR_DESCRIPTIONS = (
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_CURRENT_UV_INDEX,
        name="IMS Current UV Index",
        icon="mdi:weather-sunny",
        native_unit_of_measurement=UV_INDEX,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_UV_INDEX,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_CURRENT_UV_LEVEL,
        name="IMS Current UV Level",
        icon="mdi:weather-sunny",
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_UV_LEVEL,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_MAX_UV_INDEX,
        name="IMS Max UV Index",
        icon="mdi:weather-sunny",
        native_unit_of_measurement=UV_INDEX,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_UV_INDEX_MAX,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_CITY,
        name="IMS City",
        icon="mdi:city",
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_LOCATION,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_TEMPERATURE,
        name="IMS Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_TEMPERATURE,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FEELS_LIKE,
        name="IMS Feels Like",
        icon="mdi:water-percent",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_FEELS_LIKE,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_HUMIDITY,
        name="IMS Humidity",
        icon="mdi:weather-sunny",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_HUMIDITY,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_IS_RAINING,
        name="IMS Is Raining",
        icon="mdi:weather-rainy",
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_RAIN,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_WIND_SPEED,
        name="IMS Wind Speed",
        icon="mdi:weather-windy",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_WIND_SPEED,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_TIME,
        name="IMS Forecast Time",
        icon="mdi:weather-windy",
        device_class=SensorDeviceClass.TIMESTAMP,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_FORECAST_TIME,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_PRECIPITATION,
        name="IMS Precipitation",
        icon="mdi:weather-pouring",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_RAIN,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_PRECIPITATION_PROBABILITY,
        name="IMS Precipitation Probability",
        icon="mdi:cloud-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_RAIN_CHANCE,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_TODAY,
        name="IMS Forecast Today",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY1,
        name="IMS Forecast Day1",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY2,
        name="IMS Forecast Day2",
        icon="mdi:weather-windy",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY3,
        name="IMS Forecast Day3",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY4,
        name="IMS Forecast Day4",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY5,
        name="IMS Forecast Day5",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY6,
        name="IMS Forecast Day6",
        icon="mdi:weather-sunny",
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FORECAST_PREFIX + TYPE_FORECAST_DAY7,
        name="IMS Forecast Day7",
        icon="mdi:weather-sunny",
    ),
)


async def async_setup_platform(hass, config_entry, async_add_entities, discovery_info=None):
    _LOGGER.warning(
        "Configuration of IMS Weather sensor in YAML is deprecated "
        "Your existing configuration has been imported into the UI automatically "
        "and can be safely removed from your configuration.yaml file"
    )

    # Define as a sensor platform
    config_entry[IMS_PLATFORM] = [IMS_PLATFORMS[0]]

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

    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]

    # Add IMS Sensors
    sensors: list[Entity] = []
    # Add forecast entities
    for description in SENSOR_DESCRIPTIONS:
        sensors.append(ImsSensor(weather_coordinator, description))

    async_add_entities(sensors, update_before_add=True)


def generate_forecast_extra_state_attributes(daily_forecast):
    attributes = {
        "minimum_temperature": {
            "value": daily_forecast.minimum_temperature,
            "unit": UnitOfTemperature.CELSIUS,
        },
        "maximum_temperature": {
            "value": daily_forecast.maximum_temperature,
            "unit": UnitOfTemperature.CELSIUS,
        },
        "maximum_uvi": {"value": daily_forecast.maximum_uvi, "unit": UV_INDEX},
        "weather": {
            "value": daily_forecast.weather,
            "icon": WEATHER_CODE_TO_ICON.get(daily_forecast.weather_code, "mdi:weather-sunny"),
        },
        "description": {"value": daily_forecast.description},
        "date": {"value": daily_forecast.date.strftime("%Y/%m/%d")},
    }

    last_weather_code = None
    last_weather_status = None
    for hour in daily_forecast.hours:
        if hour.weather:
            last_weather_status = hour.weather
        elif not last_weather_status:
            last_weather_status = daily_forecast.weather

        if hour.weather_code and hour.weather_code != "0":
            last_weather_code = hour.weather_code
        elif not last_weather_code:
            last_weather_code = daily_forecast.weather_code

        attributes[hour.hour] = {
            "weather": {
                "value": last_weather_status,
                "icon": WEATHER_CODE_TO_ICON.get(last_weather_code)
            },
            "temperature": {"value": hour.temperature, "unit": UnitOfTemperature.CELSIUS},
        }

    return attributes


class ImsSensor(ImsEntity, SensorEntity):
    """Representation of an IMS sensor."""

    @callback
    def _update_from_latest_data(self) -> None:
        """Update the state."""
        data = self.coordinator.data

        if self.entity_description.forecast_mode == forecast_mode.DAILY or self.entity_description.forecast_mode == forecast_mode.HOURLY:
            if not data or not data.forecast:
                _LOGGER.warning("For %s - no data.forecast", self.entity_description.key)
                self._attr_native_value = None
                return
        elif self.entity_description.forecast_mode == forecast_mode.CURRENT:
            if not data or not data.current_weather:
                _LOGGER.warning("For %s - no data.current_weather", self.entity_description.key)
                self._attr_native_value = None
                return

        match self.entity_description.key:
            case sensor_keys.TYPE_CURRENT_UV_LEVEL:
                match data.current_weather.u_v_level:
                    case "E":
                        self._attr_native_value = UV_LEVEL_EXTREME
                    case "V":
                        self._attr_native_value = UV_LEVEL_VHIGH
                    case "H":
                        self._attr_native_value = UV_LEVEL_HIGH
                    case "M":
                        self._attr_native_value = UV_LEVEL_MODERATE
                    case _:
                        self._attr_native_value = UV_LEVEL_LOW

            case sensor_keys.TYPE_CURRENT_UV_INDEX:
                self._attr_native_value = data.current_weather.u_v_index

            case sensor_keys.TYPE_MAX_UV_INDEX:
                self._attr_native_value = data.current_weather.u_v_i_max

            case sensor_keys.TYPE_CITY:
                _LOGGER.info("Location: %s, entity: %s", data.current_weather.location, self.entity_description.key)
                self._attr_native_value = data.current_weather.location

            case sensor_keys.TYPE_TEMPERATURE:
                self._attr_native_value = data.current_weather.temperature

            case sensor_keys.TYPE_FEELS_LIKE:
                self._attr_native_value = data.current_weather.feels_like

            case sensor_keys.TYPE_HUMIDITY:
                self._attr_native_value = data.current_weather.humidity

            case sensor_keys.TYPE_IS_RAINING:
                self._attr_native_value = "raining" if (
                            data.current_weather.rain and data.current_weather.rain > 0.0) else "not_raining"

            case sensor_keys.TYPE_PRECIPITATION:
                self._attr_native_value = data.current_weather.rain if (
                            data.current_weather.rain and data.current_weather.rain > 0.0) else 0.0

            case sensor_keys.TYPE_PRECIPITATION_PROBABILITY:
                self._attr_native_value = data.current_weather.rain_chance

            case sensor_keys.TYPE_FORECAST_TIME:
                self._attr_native_value = data.current_weather.forecast_time.astimezone(timezone('Asia/Jerusalem'))

            case sensor_keys.TYPE_WIND_SPEED:
                self._attr_native_value = data.current_weather.wind_speed

            case sensor_keys.TYPE_FORECAST_TODAY | sensor_keys.TYPE_FORECAST_DAY1 | \
                 sensor_keys.TYPE_FORECAST_DAY2 | sensor_keys.TYPE_FORECAST_DAY3 | \
                 sensor_keys.TYPE_FORECAST_DAY4 | sensor_keys.TYPE_FORECAST_DAY5 | \
                 sensor_keys.TYPE_FORECAST_DAY6 | sensor_keys.TYPE_FORECAST_DAY7:
                day_index = 0 if self.entity_description.key == sensor_keys.TYPE_FORECAST_TODAY \
                    else int(self.entity_description.key[-1])
                if day_index < len(data.forecast.days):
                    daily_forecast = data.forecast.days[day_index]
                    self._attr_native_value = daily_forecast.day
                    self._attr_extra_state_attributes = generate_forecast_extra_state_attributes(daily_forecast)
                    self._attr_icon = WEATHER_CODE_TO_ICON.get(daily_forecast.weather_code, "mdi:weather-sunny")

            case _:
                self._attr_native_value = None
