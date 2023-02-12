"""Weather data coordinator for the OpenWeatherMap (OWM) service."""
from datetime import timedelta
import logging

import async_timeout

import json

import voluptuous as vol

from homeassistant.helpers import sun
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt
from weatheril import *


from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Powered by Pirate Weather"

        
class WeatherUpdateCoordinator(DataUpdateCoordinator):
    """Weather data update coordinator."""

    def __init__(self, city, language, update_interval, hass):
        """Initialize coordinator."""
        self.city = city
        self.language = language
        self.update_interval = update_interval
        self.weather  = WeatherIL(str(city),language)

        self.data = None
        self.currently = None
        self.hourly = None
        self.daily = None
        self._connect_error = False

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=update_interval
        )
               
                 
                        
    async def _async_update_data(self):
        """Update the data."""
        data = {}
        async with async_timeout.timeout(30):
            try:
                data = await self._get_ims_weather()
            except Exception as error:
                raise UpdateFailed(error) from error
        return data


    async def _get_ims_weather(self):
        """Poll weather data from IMS."""   
    
        current_weather = self.weather.get_current_analysis()
        forcast = self.weather.get_forcast()
        images = self.weather.get_radar_images()

        return WeatherData(current_weather, forcast)

class WeatherData:
    def __init__(self, current_weather, forecast, images):
        self.current_weather = current_weather.json
        self.forecast = forecast
        self.images = images.json