"""Weather data coordinator for the OpenWeatherMap (OWM) service."""

from __future__ import annotations

import asyncio
import datetime
import logging
from dataclasses import dataclass
from typing import Any

import homeassistant.util.dt as dt_util

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from weatheril import WeatherIL, Forecast, Weather, RadarSatellite, Warning

from .const import (
    DOMAIN,
    IMS_TIMEZONE,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Powered by IMS Weather"

# Use the shared timezone constant
timezone = IMS_TIMEZONE


@dataclass
class WeatherData:
    """Weather data container."""

    current_weather: Weather
    forecast: Forecast
    images: RadarSatellite
    warnings: list[Warning]


class WeatherUpdateCoordinator(DataUpdateCoordinator[WeatherData]):
    """Weather data update coordinator."""

    def __init__(
        self,
        city: int | str,
        language: str,
        update_interval: datetime.timedelta,
        hass: Any,
    ) -> None:
        """Initialize coordinator."""
        self.city = city
        self.language = language
        self.update_interval = update_interval
        self.weather = WeatherIL(str(city), language)

        self._connect_error = False
        self._hass = hass

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> WeatherData:
        """Update the data."""
        async with self._hass.timeout.async_timeout(30):
            try:
                _LOGGER.info("Fetching data from IMS")
                data = await self._get_ims_weather()
            except Exception as error:
                raise UpdateFailed(error) from error
        return data

    async def _get_ims_weather(self) -> WeatherData:
        """Poll weather data from IMS."""

        try:
            loop = asyncio.get_event_loop()
        except Exception:
            loop = asyncio.new_event_loop()

        current_weather = await loop.run_in_executor(
            None, self.weather.get_current_analysis
        )
        weather_forecast = await loop.run_in_executor(None, self.weather.get_forecast)
        warnings = await loop.run_in_executor(None, self.weather.get_warnings)
        images = await loop.run_in_executor(None, self.weather.get_radar_images)

        _LOGGER.debug(
            "Data fetched from IMS of %s",
            current_weather.forecast_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )

        self._filter_future_forecast(weather_forecast)
        return WeatherData(current_weather, weather_forecast, images, warnings)

    @staticmethod
    def _filter_future_forecast(weather_forecast: Forecast) -> None:
        """Filter Forecast to include only future dates"""
        today_datetime = dt_util.as_local(
            datetime.datetime.combine(dt_util.now(timezone).date(), datetime.time())
        )
        filtered_day_list = list(
            filter(lambda daily: daily.date >= today_datetime, weather_forecast.days)
        )

        for daily_forecast in filtered_day_list:
            filtered_hours = []
            for hourly_forecast in daily_forecast.hours:
                forecast_datetime = daily_forecast.date + datetime.timedelta(
                    hours=int(hourly_forecast.hour.split(":")[0])
                )
                if dt_util.now(timezone) <= forecast_datetime:
                    filtered_hours.append(hourly_forecast)
            daily_forecast.hours = filtered_hours

        weather_forecast.days = filtered_day_list
