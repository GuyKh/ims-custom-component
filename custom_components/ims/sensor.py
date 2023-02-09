import logging
import asyncio
from weatheril import *
import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS

CONF_UPDATE_INTERVAL = 'update_interval'
CONF_CITY = 'city'
CONF_LANGUAGE = 'language'
IMAGES_PATH = "images_path"
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CITY): cv.string,
    vol.Required(CONF_LANGUAGE): cv.string,
    vol.Required(IMAGES_PATH, default="/tmp"): cv.string,
    vol.Optional(CONF_UPDATE_INTERVAL, default=10): cv.positive_int,
})

weather  = None


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_client = ImsApiClient(config)
    entities = []
    entities.append(ImsCity(hass, config,api_client))
    entities.append(ImsTemprature(hass, config,api_client))
    entities.append(ImsRealFeel(hass, config,api_client))
    entities.append(ImsHumidity(hass, config,api_client))
    entities.append(ImsWindSpeed(hass, config,api_client))
    entities.append(ImsRain(hass, config,api_client))
    entities.append(ImsDateTime(hass, config,api_client))
    async_add_entities(entities, True)
    await entities[0].async_update()
    return True

class ImsApiClient:
    def __init__(self,config):
        self._config = config
        self.weather  = WeatherIL(self._config.get(CONF_CITY),self._config.get(CONF_LANGUAGE))
    
    def get_data(self):
        self.current_weather = self.weather.get_current_analysis()
        self.forcast = self.weather.get_forcast()
        self.images = self.weather.get_radar_images()

class ImsCity(Entity):

    def __init__(self, hass, config,api_client):
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
        if self._language =="he":
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

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._config = config
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_temprature"
        self._api_client = api_client

    @property
    def name(self):
        if self._language =="he":
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
    def icon(self):
        return "mdi:thermometer"

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    def update(self):
        self._state = self._api_client.current_weather.temperature

class ImsRealFeel(Entity):

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_realfeel"
        self._api_client = api_client
        

    @property
    def name(self):
        if self._language =="he":
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

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_humidity"
        self._api_client = api_client
        

    @property
    def name(self):
        if self._language =="he":
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

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_rain"
        self._api_client = api_client

    @property
    def name(self):
        if self._language =="he":
            return "גשם"
        else:
            return "Rain"

    @property
    def state(self):
        try:
            if self._language =="he":
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

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._city = config.get(CONF_CITY)
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_windspeed"
        self._api_client = api_client

    @property
    def name(self):
        if self._language =="he":
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
        if self._language =="he":
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

    def __init__(self, hass, config,api_client):
        self._hass = hass
        self._language = config.get(CONF_LANGUAGE)
        self._update_interval = config.get(CONF_UPDATE_INTERVAL)
        self.entity_id = f"sensor.ims_forecast_time"
        self._api_client = api_client

    @property
    def name(self):
        if self._language =="he":
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

