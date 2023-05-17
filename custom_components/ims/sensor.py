import asyncio
import json
import logging
import types
import pytz
from dataclasses import field, dataclass
from pytz import timezone

from datetime import date, datetime
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from types import SimpleNamespace
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass
)

from homeassistant.const import UV_INDEX, UnitOfTime, CONF_NAME, TEMP_CELSIUS, PERCENTAGE, SPEED_KILOMETERS_PER_HOUR
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ImsEntity
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
    TYPE_CURRENT_UV_INDEX,
    TYPE_CURRENT_UV_LEVEL,
    TYPE_MAX_UV_INDEX, FIELD_NAME_UV_INDEX, FIELD_NAME_UV_LEVEL, FIELD_NAME_UV_INDEX_MAX, TYPE_HUMIDITY,
    FIELD_NAME_HUMIDITY, FIELD_NAME_TEMPERATURE, FIELD_NAME_LOCATION, TYPE_FEELS_LIKE, FIELD_NAME_FEELS_LIKE,
    FIELD_NAME_RAIN, TYPE_WIND_SPEED, TYPE_FORECAST_TIME, FIELD_NAME_FORECAST_TIME, TYPE_CITY, TYPE_TEMPERATURE,
    TYPE_RAIN, FIELD_NAME_WIND_SPEED,
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
sensor_keys.TYPE_RAIN = IMS_SENSOR_KEY_PREFIX + TYPE_RAIN
sensor_keys.TYPE_WIND_SPEED = IMS_SENSOR_KEY_PREFIX + TYPE_WIND_SPEED

_LOGGER = logging.getLogger(__name__)

UV_LEVEL_EXTREME = "Extreme"
UV_LEVEL_VHIGH = "Very High"
UV_LEVEL_HIGH = "High"
UV_LEVEL_MODERATE = "Moderate"
UV_LEVEL_LOW = "Low"

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

@dataclass
class ImsSensorEntityDescription(SensorEntityDescription):
    """Describes Pirate Weather sensor entity."""
    field_name: str | None = None
    forecast_mode: str | None = None


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
        name="IMS Humidity",
        icon="mdi:city",
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_LOCATION,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_TEMPERATURE,
        name="IMS Temperature",
        icon="mdi:thermometer",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_TEMPERATURE,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_FEELS_LIKE,
        name="IMS RealFeel",
        icon="mdi:water-percent",
        native_unit_of_measurement=TEMP_CELSIUS,
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
        key=IMS_SENSOR_KEY_PREFIX + TYPE_RAIN,
        name="IMS Rain",
        icon="mdi:weather-rainy",
        forecast_mode=forecast_mode.CURRENT,
        field_name=FIELD_NAME_RAIN,
    ),
    ImsSensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_WIND_SPEED,
        name="IMS Wind Speed",
        icon="mdi:weather-windy",
        native_unit_of_measurement=SPEED_KILOMETERS_PER_HOUR,
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
)


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
    # sensors.append(ImsCity(hass, city, language, weather_coordinator))
    # sensors.append(ImsTemperature(hass, city, language, weather_coordinator))
    # sensors.append(ImsRealFeel(hass, city, language, weather_coordinator))
    # sensors.append(ImsHumidity(hass, city, language, weather_coordinator))
    # sensors.append(ImsWindSpeed(hass, city, language, weather_coordinator))
    # sensors.append(ImsRain(hass, city, language, weather_coordinator))
    # sensors.append(ImsDateTime(hass, language, weather_coordinator))

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

    for description in SENSOR_DESCRIPTIONS:
        sensors.append(ImsSensor(weather_coordinator, description))

    async_add_entities(sensors, update_before_add=True)

    return True


class ImsSensor(ImsEntity, SensorEntity):
    """Representation of an IMS sensor."""

    @callback
    def _update_from_latest_data(self) -> None:
        """Update the state."""
        data = self.coordinator.data

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
                self._attr_native_value = data.current_weather.location

            case sensor_keys.TYPE_TEMPERATURE:
                self._attr_native_value = data.current_weather.temperature

            case sensor_keys.TYPE_FEELS_LIKE:
                self._attr_native_value = data.current_weather.feels_like

            case sensor_keys.TYPE_HUMIDITY:
                self._attr_native_value = data.current_weather.humidity

            case sensor_keys.TYPE_RAIN:
                self._attr_native_value = "raining" if (data.current_weather.rain and data.current_weather.rain > 0.0) else "not_raining"

            case sensor_keys.TYPE_FORECAST_TIME:
                self._attr_native_value = data.current_weather.forecast_time.astimezone(timezone('Asia/Jerusalem'))

            case sensor_keys.TYPE_WIND_SPEED:
                self._attr_native_value = data.current_weather.wind_speed

            case _:
                self._attr_native_value = None

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
