"""Config flow for Pirate Weather."""
import voluptuous as vol
import logging
from datetime import timedelta

import forecastio
from forecastio.models import Forecast
import json
import aiohttp

from homeassistant import config_entries
from homeassistant.const import (
    CONF_MODE,
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_CITY,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONFIG_FLOW_VERSION,
    CONF_UPDATE_INTERVAL,
    DEFAULT_IMAGE_PATH,
    DEFAULT_FORECAST_MODE,
    DEFAULT_LANGUAGE,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    FORECAST_MODES,
    LANGUAGES,
    CONF_UNITS,
    DEFAULT_UNITS,
    FORECASTS_DAILY,
    FORECASTS_HOURLY,
    ALL_CONDITIONS,
    PW_PLATFORMS,
    PW_PLATFORM,
    PW_PREVPLATFORM,
    PW_ROUND,
)

ATTRIBUTION = "Powered by Pirate Weather"
_LOGGER = logging.getLogger(__name__)

CONF_FORECAST = "forecast"
CONF_HOURLY_FORECAST = "hourly_forecast"


class PirateWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PirateWeather."""

    VERSION = CONFIG_FLOW_VERSION

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return PirateWeatherOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        schema = vol.Schema(
          {
              vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
              vol.Required(
                  CONF_CITY, default=1
              ): str,
              vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
                  LANGUAGES
              ): str,
              vol.Optional(
                  CONF_UPDATE_INTERVAL, default=DEFAULT_SCAN_INTERVAL
              ): int,
              vol.Required(CONF_MODE, default=DEFAULT_FORECAST_MODE): vol.In(
                  FORECAST_MODES
              ),
              vol.Required(CONF_IMAGES_PATH, default="/tmp"): cv.string
          }
        ) 
        
    
        if user_input is not None:
            city = user_input[CONF_CITY]
            language = user_input[CONF_LANGUAGE]
            forecast_mode = user_input[CONF_MODE]
            entityNamee = user_input[CONF_NAME]
            image_path = user_input[CONF_IMAGES_PATH]

            
            
            # Convert scan interval to timedelta
            if isinstance(user_input[CONF_UPDATE_INTERVAL], str):
              user_input[CONF_UPDATE_INTERVAL] = cv.time_period_str(user_input[CONF_UPDATE_INTERVAL])
              
              
            # Convert scan interval to number of minutes
            if isinstance(user_input[CONF_UPDATE_INTERVAL], timedelta):
              user_input[CONF_UPDATE_INTERVAL] = user_input[CONF_UPDATE_INTERVAL].total_minutes()                        
              

            # Unique value includes the location and forcastHours/ forecastDays to seperate WeatherEntity/ Sensor            
#            await self.async_set_unique_id(f"pw-{latitude}-{longitude}-{forecastDays}-{forecastHours}-{forecastMode}-{entityNamee}")            
            await self.async_set_unique_id(f"ims-{city}-{language}-{forecastMode}-{entityNamee}")      
                        
            self._abort_if_unique_id_configured()

            
            try:
              api_status = await _is_ims_api_online(
                self.hass, user_input[CONF_LANGUAGE], user_input[CONF_CITY]
              )
              
            except:
              _LOGGER.warning("IMS Weather Setup Error: HTTP Error: " + api_status)
              errors["base"] = "API Error: " + api_status
              
            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            else:
                _LOGGER.warning(errors)
                     
        
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


    async def async_step_import(self, import_input=None):
        """Set the config entry up from yaml."""
        config = import_input.copy()
        
        if CONF_NAME not in config:
            config[CONF_NAME] = DEFAULT_NAME
        if CONF_CITY not in config:
            config[CONF_CITY] = self.hass.config.city
        if CONF_LANGUAGE not in config:
            config[CONF_LANGUAGE] = self.hass.config.language
        if CONF_MODE not in config:
            config[CONF_MODE] = DEFAULT_FORECAST_MODE
        if CONF_LANGUAGE not in config:
            config[CONF_LANGUAGE] = DEFAULT_LANGUAGE 
        if CONF_UPDATE_INTERVAL not in config:
            config[CONF_UPDATE_INTERVAL] =  DEFAULT_SCAN_INTERVAL                                     
        if CONF_IMAGES_PATH not in config:
            config[CONF_IMAGES_PATH] = DEFAULT_IMAGE_PATH
        return await self.async_step_user(config)


class PirateWeatherOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            entry = self.config_entry
            
            #if self.config_entry.options:
            #  user_input[PW_PREVPLATFORM] = self.config_entry.options[PW_PLATFORM]
            #else:
            #user_input[PW_PREVPLATFORM] = self.hass.data[DOMAIN][entry.entry_id][PW_PLATFORM]
            #self.hass.data[DOMAIN][entry.entry_id][PW_PREVPLATFORM] = self.hass.data[DOMAIN][entry.entry_id][PW_PLATFORM]
            #user_input[PW_PREVPLATFORM] = self.hass.data[DOMAIN][entry.entry_id][PW_PLATFORM]
            #_LOGGER.warning('async_step_init_Options')
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
              {
                vol.Optional(
                    CONF_NAME,
                     default=self.config_entry.options.get(
                       CONF_NAME,
                       self.config_entry.data.get(CONF_NAME, DEFAULT_NAME),
                       ),
                       ): str,      
                vol.Optional(
                    CONF_CITY,
                     default=self.config_entry.options.get(
                       CONF_CITY,
                       self.config_entry.data.get(CONF_CITY, self.hass.config.city),
                       ),
                       ): str,
                vol.Optional(
                    CONF_LANGUAGE,
                    default=self.config_entry.options.get(
                        CONF_LANGUAGE,
                        self.config_entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                    ),
                ): vol.In(LANGUAGES)                                                                 
                vol.Optional(
                    CONF_MODE,
                    default=self.config_entry.options.get(
                        CONF_MODE,
                        self.config_entry.data.get(CONF_MODE, DEFAULT_FORECAST_MODE),
                    ),
                ): vol.In(FORECAST_MODES),
                vol.Optional(
                    CONF_IMAGES_PATH,
                    default=self.config_entry.options.get(
                        CONF_IMAGES_PATH,
                        self.config_entry.data.get(CONF_IMAGES_PATH, DEFAULT_IMAGE_PATH),
                    ),
                ): str
            ),
        )

async def _is_ims_api_online(hass, language, city):
      forecastString = "https://ims.gov.il/" + language + /forecast_data/" + str(city)
  
      async with aiohttp.ClientSession(raise_for_status=False) as session:
        async with session.get(forecastString) as resp:
          resptext = await resp.text()
          jsonText = json.loads(resptext)
          headers = resp.headers
          status = resp.status
      
      return status