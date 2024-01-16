"""Weather data coordinator for the OpenWeatherMap (OWM) service."""
import asyncio
import logging
from datetime import timedelta, date

import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from weatheril import *

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Powered by IMS Weather"


class WeatherUpdateCoordinator(DataUpdateCoordinator):
    """Weather data update coordinator."""

    def __init__(self, city, language, update_interval, hass):
        """Initialize coordinator."""
        self.city = city
        self.language = language
        self.update_interval = update_interval
        self.weather = WeatherIL(str(city), language)

        self.data = None
        self._connect_error = False

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

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

        loop = None
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()

        current_weather = await loop.run_in_executor(
            None, self.weather.get_current_analysis
        )
        weather_forecast = await loop.run_in_executor(None, self.weather.get_forecast)
        images = await loop.run_in_executor(None, self.weather.get_radar_images)

        _LOGGER.debug("Data fetched from IMS of %s", current_weather.forecast_time.strftime("%m/%d/%Y, %H:%M:%S"))

        self._filter_future_forecast(weather_forecast)
        return WeatherData(current_weather, weather_forecast, images)

    @staticmethod
    def _filter_future_forecast(weather_forecast):
        """ Filter Forecast to include only future dates """
        today_datetime = datetime.fromordinal(date.today().toordinal())
        filtered_day_list = list(filter(lambda daily: daily.date >= today_datetime, weather_forecast.days))

        for daily_forecast in filtered_day_list:
            filtered_hours = []
            for hourly_forecast in daily_forecast.hours:
                forecast_datetime = daily_forecast.date + timedelta(hours=int(hourly_forecast.hour.split(":")[0]))
                if datetime.now() <= forecast_datetime:
                    filtered_hours.append(hourly_forecast)
            daily_forecast.hours = filtered_hours

        weather_forecast.days = filtered_day_list


class WeatherData:
    def __init__(self, current_weather, weather_forecast, images):
        self.current_weather = current_weather
        self.forecast = weather_forecast
        self.images = images
