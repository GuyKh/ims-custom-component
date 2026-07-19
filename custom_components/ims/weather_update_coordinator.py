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
    WARNING_SENSOR_KEYS,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Powered by IMS Weather"

# Use the shared timezone constant
timezone = IMS_TIMEZONE


@dataclass
class WeatherData:
    """Weather data container."""

    current_weather: Weather
    forecast: Forecast | None
    images: RadarSatellite | None
    warnings: list[Warning]


class WeatherUpdateCoordinator(DataUpdateCoordinator[WeatherData]):
    """Weather data update coordinator."""

    def __init__(
        self,
        city: int | str,
        language: str,
        update_interval: datetime.timedelta,
        hass: Any,
        monitored_conditions: list[str] | None = None,
    ) -> None:
        """Initialize coordinator.

        ``monitored_conditions`` is the list of sensor keys the user has
        enabled for this config entry. When none of them consume
        ``WeatherData.warnings``, the coordinator skips the warnings HTTP
        fetch entirely. ``None`` (the default) means "no conditions were
        stored" and is treated as "all sensors enabled" — the legacy
        behavior in ``sensor.py`` and ``binary_sensor.py`` falls back to
        every description key when conditions are missing.
        """
        self.city = city
        self.language = language
        self.update_interval = update_interval
        self.weather = WeatherIL(str(city), language)

        self._connect_error = False
        self._hass = hass
        self._monitored_conditions: list[str] | None = monitored_conditions

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
        weather_forecast = await self._fetch_forecast(loop)
        warnings = (
            await self._fetch_warnings(loop) if self._should_fetch_warnings() else []
        )
        images = await self._fetch_radar_images(loop)

        _LOGGER.debug(
            "Data fetched from IMS of %s",
            current_weather.forecast_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )

        if weather_forecast is not None:
            self._filter_future_forecast(weather_forecast)
        else:
            _LOGGER.warning(
                "IMS returned no forecast data; continuing without forecast"
            )
        return WeatherData(current_weather, weather_forecast, images, warnings)

    async def _fetch_forecast(self, loop: asyncio.AbstractEventLoop) -> Forecast | None:
        """Fetch weather forecast from IMS.

        Non-fatal: returns ``None`` on any failure (timeout, network error,
        parse error, server outage) so a misbehaving forecast endpoint cannot
        prevent the rest of the update from completing.  The upstream
        ``weatheril`` library may raise ``AttributeError`` when the IMS API
        returns unexpected data (e.g. ``None`` hourly payload).
        """
        try:
            return await loop.run_in_executor(None, self.weather.get_forecast)
        except Exception as error:  # noqa: BLE001 - intentional, see docstring
            _LOGGER.warning(
                "Failed to fetch IMS weather forecast; continuing without it: %s",
                error,
            )
            return None

    async def _fetch_warnings(self, loop: asyncio.AbstractEventLoop) -> list[Warning]:
        """Fetch active IMS weather warnings.

        Non-fatal: returns an empty list on any failure (timeout, network
        error, parse error, server outage) so a misbehaving warnings
        endpoint cannot prevent the rest of the update from completing.
        Downstream consumers (sensor, binary_sensor) handle an empty
        list as "no active warnings".

        Callers should gate this method with ``_should_fetch_warnings()``
        so the HTTP round-trip is avoided entirely when no sensor in the
        current config entry consumes warnings.
        """
        try:
            return await loop.run_in_executor(None, self.weather.get_warnings)
        except Exception as error:  # noqa: BLE001 - intentional, see docstring
            _LOGGER.warning(
                "Failed to fetch IMS weather warnings; continuing with no active warnings: %s",
                error,
            )
            return []

    async def _fetch_radar_images(
        self, loop: asyncio.AbstractEventLoop
    ) -> RadarSatellite | None:
        """Fetch IMS radar/satellite imagery.

        Non-fatal: returns ``None`` on any failure (timeout, network error,
        parse error, server outage) so a misbehaving radar endpoint cannot
        prevent the rest of the update from completing. ``WeatherData.images``
        is typed as ``RadarSatellite | None`` to reflect this.
        """
        try:
            return await loop.run_in_executor(None, self.weather.get_radar_images)
        except Exception as error:  # noqa: BLE001 - intentional, see docstring
            _LOGGER.warning(
                "Failed to fetch IMS radar/satellite imagery; continuing without it: %s",
                error,
            )
            return None

    def _should_fetch_warnings(self) -> bool:
        """Return True if any enabled sensor consumes ``data.warnings``.

        ``None`` ``monitored_conditions`` falls back to the legacy
        "all sensors enabled" behavior (see ``__init__``). An empty list
        means "no sensors enabled" and yields ``False``.
        """
        conditions = self._monitored_conditions
        if conditions is None:
            return True
        return any(key in WARNING_SENSOR_KEYS for key in conditions)

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
