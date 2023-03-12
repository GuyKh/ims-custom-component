"""Consts for the OpenWeatherMap."""
from __future__ import annotations
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_EXCEPTIONAL,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_WINDY,
    ATTR_CONDITION_WINDY_VARIANT,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_PRESSURE,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
)
from homeassistant.const import (
    DEGREE,
    LENGTH_MILLIMETERS,
    PERCENTAGE,
    PRESSURE_HPA,
    SPEED_METERS_PER_SECOND,
    TEMP_CELSIUS,
    UV_INDEX,
    Platform,
)

DOMAIN = "ims"
DEFAULT_NAME = "IMS Weather"
DEFAULT_LANGUAGE = "en"
DEFAULT_UPDATE_INTERVAL = 60
DEFAULT_IMAGE_PATH = "/tmp"
ATTRIBUTION = "Data provided by Israel Meteorological Service"
MANUFACTURER = "IMS"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_CITY = "city"
CONF_LANGUAGE = "language"
CONF_MODE = "mode"
CONF_IMAGES_PATH = "images_path"
CONFIG_FLOW_VERSION = 2
ENTRY_NAME = "name"
ENTRY_WEATHER_COORDINATOR = "weather_coordinator"
ATTR_API_PRECIPITATION = "precipitation"
ATTR_API_FORECAST_TIME = "forecast_time"
ATTR_API_DEW_POINT = "due_point_Temp"
ATTR_API_TEMPERATURE = "temperature"
ATTR_API_FEELS_LIKE_TEMPERATURE = "feels_like"
ATTR_API_WIND_SPEED = "wind_speed"
ATTR_API_WIND_BEARING = "wind_direction_id"
ATTR_API_WIND_CHILL = "wind_chill"
ATTR_API_RELATIVE_HUMIDITY = "relative_humidity"
ATTR_API_RAIN = "rain"
ATTR_API_UV_INDEX = "u_v_index"
ATTR_API_UV_LEVEL = "u_v_level"
ATTR_API_WEATHER_CODE = "weather_code"
ATTR_API_HEAT_STRESS = "heat_stress"
ATTR_API_HEAT_STRESS_LEVEL = "heat_stress_level"
ATTR_API_FORECAST_DATE = "forecast_date"
ATTR_API_MAXIMUM_TEMPERATURE = "maximum_temperature"
ATTR_API_MINIMUM_TEMPERATURE = "minimum_temperature"
ATTR_API_MAXIMUM_UV_INDEX = "maximum_uvi"
UPDATE_LISTENER = "update_listener"
PLATFORMS = [Platform.SENSOR, Platform.WEATHER]
IMS_PLATFORMS = ["Sensor", "Weather"]
IMS_PLATFORM = "ims_platform"
IMS_PREVPLATFORM = "ims_prevplatform"

FORECAST_MODE_HOURLY = "hourly"
FORECAST_MODE_DAILY = "daily"
DEFAULT_FORECAST_MODE = FORECAST_MODE_DAILY
FORECAST_MODES = [FORECAST_MODE_HOURLY, FORECAST_MODE_DAILY]

LANGUAGES = ["en", "he"]

# Based on https://ims.gov.il/en/wind_directions
WIND_DIRECTIONS = {
    1: float(180),
    2: float(203),
    3: float(225),
    4: float(248),
    5: float(270),
    6: float(293),
    7: float(315),
    8: float(338),
    9: float(360),
    10: float(23),
    11: float(45),
    12: float(68),
    13: float(90),
    14: float(113),
    15: float(135),
    16: float(158),
    17: float(180),
}

# Based on https://ims.gov.il/en/weather_codes
WEATHER_CODE_TO_CONDITION = {
    None: None,
    "1020": ATTR_CONDITION_LIGHTNING_RAINY,
    "1060": ATTR_CONDITION_SNOWY,
    "1070": ATTR_CONDITION_SNOWY,
    "1080": ATTR_CONDITION_SNOWY_RAINY,
    "1140": ATTR_CONDITION_RAINY,
    "1160": ATTR_CONDITION_FOG,
    "1220": ATTR_CONDITION_PARTLYCLOUDY,
    "1230": ATTR_CONDITION_CLOUDY,
    "1250": ATTR_CONDITION_SUNNY,
    "1260": ATTR_CONDITION_WINDY,
    "1270": ATTR_CONDITION_SUNNY,
    "1300": ATTR_CONDITION_HAIL,
    "1310": ATTR_CONDITION_SUNNY,
    "1320": ATTR_CONDITION_HAIL,
    "1510": ATTR_CONDITION_LIGHTNING_RAINY,
    "1520": ATTR_CONDITION_SNOWY,
    "1530": ATTR_CONDITION_PARTLYCLOUDY,
    "1540": ATTR_CONDITION_PARTLYCLOUDY,
    "1560": ATTR_CONDITION_RAINY,
    "1570": ATTR_CONDITION_WINDY_VARIANT,
    "1580": ATTR_CONDITION_EXCEPTIONAL,
    "1590": ATTR_CONDITION_EXCEPTIONAL,
}

WEATHER_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_API_DEW_POINT,
        name="Dew Point Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_TEMPERATURE,
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_RELATIVE_HUMIDITY,
        name="Relative humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_FEELS_LIKE_TEMPERATURE,
        name="Feels like temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_WIND_SPEED,
        name="Wind speed",
        native_unit_of_measurement=SPEED_METERS_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_WIND_BEARING,
        name="Wind bearing",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_WIND_CHILL,
        name="Wind chill",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_RAIN,
        name="Rain",
        native_unit_of_measurement=LENGTH_MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_UV_INDEX,
        name="UV Index",
        native_unit_of_measurement=UV_INDEX,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_UV_LEVEL,
        name="UV level",
        native_unit_of_measurement=UV_INDEX,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_WEATHER_CODE,
        name="Weather Code",
    ),
    SensorEntityDescription(
        key=ATTR_API_HEAT_STRESS,
        name="Heat Stress",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key=ATTR_API_HEAT_STRESS_LEVEL,
        name="Heat Stress Level",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
FORECAST_HOURLY_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_FORECAST_TEMP,
        name="Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=ATTR_API_WEATHER_CODE,
        name="Weather Code",
    ),
    SensorEntityDescription(
        key=ATTR_FORECAST_TIME,
        name="Forecast Time",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)
FORECAST_DAILY_SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=ATTR_API_MAXIMUM_TEMPERATURE,
        name="Maximum temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=ATTR_API_MINIMUM_TEMPERATURE,
        name="Minimum temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
    ),
    SensorEntityDescription(
        key=ATTR_API_MAXIMUM_UV_INDEX,
        name="Miximum UV index",
        native_unit_of_measurement=UV_INDEX,
    ),
    SensorEntityDescription(
        key=ATTR_API_WEATHER_CODE,
        name="Weather Code",
    ),
    SensorEntityDescription(
        key=ATTR_API_FORECAST_DATE,
        name="Forecast date",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)
