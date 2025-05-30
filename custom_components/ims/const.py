"""Consts for the OpenWeatherMap."""

from __future__ import annotations
import types

from homeassistant.components.weather import (
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_EXCEPTIONAL,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_WINDY,
)
from homeassistant.const import (
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
ATTR_API_DEW_POINT = "due_point_Temp"
ATTR_API_FEELS_LIKE_TEMPERATURE = "feels_like"
ATTR_API_FORECAST_DATE = "forecast_date"
ATTR_API_FORECAST_TIME = "forecast_time"
ATTR_API_HEAT_STRESS = "heat_stress"
ATTR_API_HEAT_STRESS_LEVEL = "heat_stress_level"
ATTR_API_MAXIMUM_TEMPERATURE = "maximum_temperature"
ATTR_API_MAXIMUM_UV_INDEX = "maximum_uvi"
ATTR_API_MINIMUM_TEMPERATURE = "minimum_temperature"
ATTR_API_PRECIPITATION = "precipitation"
ATTR_API_RAIN = "rain"
ATTR_API_RELATIVE_HUMIDITY = "relative_humidity"
ATTR_API_TEMPERATURE = "temperature"
ATTR_API_UV_INDEX = "u_v_index"
ATTR_API_UV_LEVEL = "u_v_level"
ATTR_API_WEATHER_CODE = "weather_code"
ATTR_API_WIND_BEARING = "wind_direction_id"
ATTR_API_WIND_CHILL = "wind_chill"
ATTR_API_WIND_SPEED = "wind_speed"
UPDATE_LISTENER = "update_listener"
PLATFORMS = [Platform.SENSOR, Platform.WEATHER, Platform.BINARY_SENSOR]
IMS_PLATFORMS = ["Sensor", "Weather"]
IMS_PLATFORM = "ims_platform"
IMS_PREVPLATFORM = "ims_prevplatform"

FORECAST_MODE_HOURLY = "hourly"
FORECAST_MODE_DAILY = "daily"
DEFAULT_FORECAST_MODE = FORECAST_MODE_DAILY
FORECAST_MODES = [FORECAST_MODE_HOURLY, FORECAST_MODE_DAILY]

TYPE_CITY = "city"
TYPE_CURRENT_UV_INDEX = "current_uv_index"
TYPE_CURRENT_UV_LEVEL = "current_uv_level"
TYPE_DEW_POINT_TEMP = "dew_point_temp"
TYPE_FEELS_LIKE = "feels_like"
TYPE_FORECAST_PREFIX = "forecast_"
TYPE_FORECAST_TODAY = "today"
TYPE_FORECAST_DAY1 = "day1"
TYPE_FORECAST_DAY2 = "day2"
TYPE_FORECAST_DAY3 = "day3"
TYPE_FORECAST_DAY4 = "day4"
TYPE_FORECAST_DAY5 = "day5"
TYPE_FORECAST_DAY6 = "day6"
TYPE_FORECAST_DAY7 = "day7"
TYPE_FORECAST_TIME = "forecast_time"
TYPE_HEAT_STRESS = "heat_stress"
TYPE_HEAT_STRESS_LEVEL = "heat_stress_level"
TYPE_HUMIDITY = "humidity"
TYPE_IS_RAINING = "is_raining"
TYPE_MAX_TEMP = "max_temp"
TYPE_MAX_UV_INDEX = "max_uv_index"
TYPE_MIN_TEMP = "min_temp"
TYPE_PRECIPITATION = "precipitation"
TYPE_PRECIPITATION_PROBABILITY = "precipitation_probability"
TYPE_PM10 = "pm10"
TYPE_TEMPERATURE = "temperature"
TYPE_WAVE_HEIGHT = "wave_height"
TYPE_WEATHER_CODE = "weather_code"
TYPE_WIND_CHILL = "wind_chill"
TYPE_WIND_DIRECTION = "wind_direction"
TYPE_WIND_SPEED = "wind_speed"

FIELD_NAME_DEW_POINT_TEMP = "due_point_temp"
FIELD_NAME_FEELS_LIKE = "feels_like"
FIELD_NAME_FORECAST_TIME = "forecast_time"
FIELD_NAME_HEAT_STRESS = "heat_stress"
FIELD_NAME_HEAT_STRESS_LEVEL = "heat_stress_level"
FIELD_NAME_HUMIDITY = "relative_humidity"
FIELD_NAME_LOCATION = "location"
FIELD_NAME_MAX_TEMP = "max_temp"
FIELD_NAME_MIN_TEMP = "min_temp"
FIELD_NAME_PM10 = "pm10"
FIELD_NAME_RAIN = "rain"
FIELD_NAME_RAIN_CHANCE = "rain_chance"
FIELD_NAME_TEMPERATURE = "temperature"
FIELD_NAME_UV_INDEX = "u_v_index"
FIELD_NAME_UV_INDEX_FACTOR = "u_v_i_factor"
FIELD_NAME_UV_INDEX_MAX = "u_v_i_max"
FIELD_NAME_UV_LEVEL = "u_v_level"
FIELD_NAME_WAVE_HEIGHT = "wave_height"
FIELD_NAME_WEATHER_CODE = "weather_code"
FIELD_NAME_WIND_CHILL = "wind_chill"
FIELD_NAME_WIND_DIRECTION_ID = "wind_direction_id"
FIELD_NAME_WIND_SPEED = "wind_speed"

LANGUAGES = ["en", "he"]

IMS_SENSOR_KEY_PREFIX = "ims_"


FORECAST_MODE = types.SimpleNamespace()
FORECAST_MODE.CURRENT = "current"
FORECAST_MODE.DAILY = "daily"
FORECAST_MODE.HOURLY = "hourly"


UV_LEVEL_EXTREME = "extreme"
UV_LEVEL_VHIGH = "very_high"
UV_LEVEL_HIGH = "high"
UV_LEVEL_MODERATE = "moderate"
UV_LEVEL_LOW = "low"

# Based on https://ims.gov.il/en/wind_directions
WIND_DIRECTIONS = {
    None: None,
    0: None,
    1: float(360),
    2: float(23),
    3: float(45),
    4: float(68),
    5: float(90),
    6: float(113),
    7: float(135),
    8: float(150),
    9: float(180),
    10: float(203),
    11: float(225),
    12: float(248),
    13: float(270),
    14: float(293),
    15: float(315),
    16: float(338),
    17: float(0),
}

# Based on https://ims.gov.il/en/weather_codes
WEATHER_CODE_TO_CONDITION = {
    None: None,
    "None": None,
    "0": None,
    "1010": ATTR_CONDITION_EXCEPTIONAL,
    "1020": ATTR_CONDITION_LIGHTNING_RAINY,
    "1060": ATTR_CONDITION_SNOWY,
    "1070": ATTR_CONDITION_SNOWY,
    "1080": ATTR_CONDITION_SNOWY_RAINY,
    "1140": ATTR_CONDITION_POURING,
    "1160": ATTR_CONDITION_FOG,
    "1220": ATTR_CONDITION_PARTLYCLOUDY,
    "1220-night": ATTR_CONDITION_PARTLYCLOUDY,  # no "-night"
    "1230": ATTR_CONDITION_CLOUDY,
    "1250": ATTR_CONDITION_SUNNY,
    "1250-night": ATTR_CONDITION_CLEAR_NIGHT,
    "1260": ATTR_CONDITION_WINDY,
    "1270": ATTR_CONDITION_SUNNY,
    "1300": ATTR_CONDITION_HAIL,
    "1310": ATTR_CONDITION_SUNNY,
    "1320": ATTR_CONDITION_HAIL,
    "1510": ATTR_CONDITION_LIGHTNING_RAINY,
    "1520": ATTR_CONDITION_SNOWY,
    "1530": ATTR_CONDITION_RAINY,
    "1540": ATTR_CONDITION_RAINY,
    "1560": ATTR_CONDITION_RAINY,
    "1570": ATTR_CONDITION_EXCEPTIONAL,
    "1580": ATTR_CONDITION_EXCEPTIONAL,
    "1590": ATTR_CONDITION_EXCEPTIONAL,
}


WEATHER_CODE_TO_ICON = {
    "1010": "mdi:weather-dust",
    "1020": "mdi:weather-lightning-rainy",
    "1060": "mdi:weather-snowy",
    "1070": "mdi:weather-snowy",
    "1080": "mdi:weather-snowy-rainy",
    "1140": "mdi:weather-pouring",
    "1160": "mdi:weather-fog",
    "1220": "mdi:weather-partly-cloudy",
    "1220-night": "mdi:weather-partly-cloudy-night",
    "1230": "mdi:weather-cloudy",
    "1250": "mdi:weather-sunny",
    "1250-night": "mdi:clear-night",
    "1260": "mdi:weather-windy",
    "1270": "mdi:weather-fog",
    "1300": "mdi:snowflake-melt",
    "1310": "mdi:weather-sunny-alert",
    "1320": "mdi:snowflake-alert",
    "1510": "mdi:weather-lightning",
    "1520": "mdi:weather-snowy-heavy",
    "1530": "mdi:weather-partly-rainy",
    "1540": "mdi:weather-rainy",
    "1560": "mdi:weather-rainy",
    "1570": "mdi:weather-dust",
    "1580": "mdi:weather-sunny-alert",
    "1590": "mdi:snowflake-alert",
}
