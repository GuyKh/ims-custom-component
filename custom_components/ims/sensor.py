import logging
import asyncio
from weatheril import *
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS

CONF_UPDATE_INTERVAL = "update_interval"
CONF_CITY = "city"
CONF_LANGUAGE = "language"
IMAGES_PATH = "images_path"
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CITY): cv.string,
        vol.Required(CONF_LANGUAGE): cv.string,
        vol.Required(IMAGES_PATH, default="/tmp"): cv.string,
        vol.Optional(CONF_UPDATE_INTERVAL, default=10): cv.positive_int,
    }
)

weather = None


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # Init the API Client
    api_client = ImsApiClient(config)
    # Add Ims Entities
    entities = []
    entities.append(ImsCity(hass, config, api_client))
    entities.append(ImsTemprature(hass, config, api_client))
    entities.append(ImsRealFeel(hass, config, api_client))
    entities.append(ImsHumidity(hass, config, api_client))
    entities.append(ImsWindSpeed(hass, config, api_client))
    entities.append(ImsRain(hass, config, api_client))
    entities.append(ImsDateTime(hass, config, api_client))
    async_add_entities(entities, True)
    # Call the update method to grab data from the api
    await entities[0].async_update()

    # Add forecast entities
    async_add_entities(
        [Imsforecast(hass, config, api_client, "today", api_client.forecast.days[0])],
        True,
    )
    async_add_entities(
        [Imsforecast(hass, config, api_client, "day1", api_client.forecast.days[1])],
        True,
    )
    async_add_entities(
        [Imsforecast(hass, config, api_client, "day2", api_client.forecast.days[2])],
        True,
    )
    async_add_entities(
        [Imsforecast(hass, config, api_client, "day3", api_client.forecast.days[3])],
        True,
    )
    async_add_entities(
        [Imsforecast(hass, config, api_client, "day4", api_client.forecast.days[4])],
        True,
    )

    # _LOGGER.error("Test: " + api_client.forecast.days[0].weather)
    return True


class ImsApiClient:
    def __init__(self, config):
        self._config = config
        self.weather = WeatherIL(
            self._config.get(CONF_CITY), self._config.get(CONF_LANGUAGE)
        )

    def get_data(self):
        self.current_weather = self.weather.get_current_analysis()
        self.forecast = self.weather.get_forecast()
        self.images = self.weather.get_radar_images()


class ImsCity(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._config = config
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_city"
        self._api_client = api_client
        # self._api_client.get_data()

    @property
    def name(self):
        if self._language == "he":
            return "ישוב"
        else:
            return "City"

    @property
    def state(self):
        return self._api_client.weather.get_location_name_by_id(self._city)

    @property
    def icon(self):
        return "mdi:city"

    async def async_update(self):
        await self._hass.async_add_executor_job(self.update)

    def update(self):
        self._api_client.get_data()
        self._state = self._api_client.weather.get_location_name_by_id(self._city)


class ImsTemprature(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._config = config
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_temprature"
        self._api_client = api_client

    @property
    def name(self):
        if self._language == "he":
            return "טמפרטורה"
        else:
            return "Temprature"

    @property
    def state(self):
        try:
            return self._api_client.current_weather.temperature
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
        self._state = self._api_client.current_weather.temperature


class ImsRealFeel(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_realfeel"
        self._api_client = api_client

    @property
    def name(self):
        if self._language == "he":
            return "מרגיש כמו"
        else:
            return "Real Feel"

    @property
    def state(self):
        try:
            return self._api_client.current_weather.feels_like
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
        self._state = self._api_client.current_weather.feels_like


class ImsHumidity(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_humidity"
        self._api_client = api_client

    @property
    def name(self):
        if self._language == "he":
            return "לחות"
        else:
            return "Humidity"

    @property
    def state(self):
        try:
            return self._api_client.current_weather.humidity
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
        self._state = self._api_client.current_weather.humidity


class ImsRain(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_rain"
        self._api_client = api_client

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
                if self._api_client.current_weather.rain == None:
                    return "לא יורד"
                else:
                    return "יורד"
            else:
                if self._api_client.current_weather.rain == None:
                    return "Not Raining"
                else:
                    return "Raining"
        except:
            pass

    @property
    def icon(self):
        return "mdi:weather-rainy"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._api_client.current_weather.wind_speed


class ImsWindSpeed(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_windspeed"
        self._api_client = api_client

    @property
    def name(self):
        if self._language == "he":
            return "מהירות רוח"
        else:
            return "Wind Speed"

    @property
    def state(self):
        try:
            return self._api_client.current_weather.wind_speed
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
        self._state = self._api_client.current_weather.wind_speed


class ImsDateTime(Entity):
    def __init__(self, hass, config, api_client):
        self._hass = hass
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_forecast_time"
        self._api_client = api_client

    @property
    def name(self):
        if self._language == "he":
            return "תאריך"
        else:
            return "Date"

    @property
    def state(self):
        try:
            return self._api_client.current_weather.forecast_time
        except:
            pass

    @property
    def icon(self):
        return "mdi:calendar"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._api_client.current_weather.forecast_time


class Imsforecast(Entity):
    def __init__(self, hass, config, api_client, sensor_name, forecast):
        self._hass = hass
        self._forecast = forecast
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_forecast_" + sensor_name
        self._name = sensor_name
        self._api_client = api_client
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
        date = self._forecast.date.split("-")
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
            "date": {"value": date[2] + "/" + date[1] + "/" + date[0]},
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
