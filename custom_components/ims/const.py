"""Consts for the OpenWeatherMap."""
from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_EXCEPTIONAL,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_WINDY,
    ATTR_CONDITION_WINDY_VARIANT,
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

TYPE_CURRENT_UV_INDEX = "current_uv_index"
TYPE_CURRENT_UV_LEVEL = "current_uv_level"
TYPE_MAX_UV_INDEX = "max_uv_index"
TYPE_HEAT_STRESS = "heat_stress"
TYPE_HEAT_STRESS_LEVEL = "heat_stress_level"
TYPE_HUMIDITY = "humidity"
TYPE_DEW_POINT_TEMP = "dew_point_temp"
TYPE_RAIN = "rain"
TYPE_RAIN_CHANCE = "rain_chance"
TYPE_TEMPERATURE = "temperature"
TYPE_FEELS_LIKE = "feels_like"
TYPE_MIN_TEMP = "min_temp"
TYPE_MAX_TEMP = "max_temp"
TYPE_WAVE_HEIGHT = "wave_height"
TYPE_WIND_DIRECTION = "wind_direction"
TYPE_WIND_SPEED = "wind_speed"
TYPE_WIND_CHILL = "wind_chill"
TYPE_WEATHER_CODE = "weather_code"
TYPE_CITY = "city"
TYPE_FORECAST_TIME = "forecast_time"
TYPE_FORECAST_PREFIX = "forecast_"
TYPE_FORECAST_TODAY = "today"
TYPE_FORECAST_DAY1 = "day1"
TYPE_FORECAST_DAY2 = "day2"
TYPE_FORECAST_DAY3 = "day3"
TYPE_FORECAST_DAY4 = "day4"
TYPE_FORECAST_DAY5 = "day5"
TYPE_FORECAST_DAY6 = "day6"
TYPE_FORECAST_DAY7 = "day7"

FIELD_NAME_FORECAST_TIME = "forecast_time"
FIELD_NAME_HEAT_STRESS = "heat_stress"
FIELD_NAME_HEAT_STRESS_LEVEL = "heat_stress_level"
FIELD_NAME_HUMIDITY = "relative_humidity"
FIELD_NAME_DEW_POINT_TEMP = "due_point_Temp"
FIELD_NAME_RAIN = "rain"
FIELD_NAME_RAIN_CHANCE = "rain_chance"
FIELD_NAME_TEMPERATURE = "temperature"
FIELD_NAME_FEELS_LIKE = "feels_like"
FIELD_NAME_MIN_TEMP = "min_temp"
FIELD_NAME_MAX_TEMP = "max_temp"
FIELD_NAME_WAVE_HEIGHT = "wave_height"
FIELD_NAME_WIND_DIRECTION_ID = "wind_direction_id"
FIELD_NAME_WIND_SPEED = "wind_speed"
FIELD_NAME_WIND_CHILL = "wind_chill"
FIELD_NAME_WEATHER_CODE = "weather_code"
FIELD_NAME_UV_LEVEL = "u_v_level"
FIELD_NAME_UV_INDEX = "u_v_index"
FIELD_NAME_UV_INDEX_MAX = "u_v_i_max"
FIELD_NAME_LOCATION = "location"
FIELD_NAME_UV_INDEX_FACTOR = "u_v_i_factor"

LANGUAGES = ["en", "he"]

# Based on https://ims.gov.il/en/wind_directions
WIND_DIRECTIONS = {
    0: None,
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
    "0": None,
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


WEATHER_CODE_TO_ICON = {
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
    "1140": "mdi:weather-pouring",
    "1020": "mdi:weather-lightning-rainy",
    "1510": "mdi:weather-lightning",
    "1260": "mdi:weather-windy",
    "1080": "mdi:weather-snowy-rainy",
    "1070": "mdi:weather-snowy-rainy",
    "1060": "mdi:weather-snowy",
    "1520": "mdi:weather-snowy-heavy",
}
