import logging
from typing import Any

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_registry import EntityRegistry

from datetime import timedelta

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry

from homeassistant.const import (
    CONF_MODE,
    CONF_NAME,
    Platform,
)
from homeassistant.core import HomeAssistant

from .const import (
    CONF_CITY,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONF_UPDATE_INTERVAL,
    CONFIG_FLOW_VERSION,
    DOMAIN,
    DEFAULT_FORECAST_MODE,
    ENTRY_NAME,
    ENTRY_WEATHER_COORDINATOR,
    FORECAST_MODES,
    UPDATE_LISTENER,
)

CONF_FORECAST = "forecast"
CONF_HOURLY_FORECAST = "hourly_forecast"

# from .weather_update_coordinator import WeatherUpdateCoordinator, DarkSkyData
from .weather_update_coordinator import WeatherUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
ATTRIBUTION = "Powered by Pirate Weather"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pirate Weather as config entry."""
    name = entry.data[CONF_NAME]
    city = _get_config_value(entry, CONF_CITY)
    forecast_mode = _get_config_value(entry, CONF_MODE)
    images_path = _get_config_value(entry, CONF_IMAGES_PATH)
    language = _get_config_value(entry, CONF_LANGUAGE)
    ims_scan_Int = entry.data[CONF_UPDATE_INTERVAL]

    # Extract list of int from forecast days/ hours string if present
    # _LOGGER.warning('forecast_days_type: ' + str(type(forecast_days)))

    unique_location = f"ims-{language}-{city}"

    hass.data.setdefault(DOMAIN, {})
    # If coordinator already exists for this API key, we'll use that, otherwise
    # we have to create a new one
    if unique_location in hass.data[DOMAIN]:
        weather_coordinator = hass.data[DOMAIN].get(unique_location)
        _LOGGER.info(
            "An existing IMS weather coordinator already exists for this location. Using that one instead"
        )
    else:
        weather_coordinator = WeatherUpdateCoordinator(
            city, language, timedelta(minutes=ims_scan_Int), hass
        )
        hass.data[DOMAIN][unique_location] = weather_coordinator
        # _LOGGER.warning('New Coordinator')

    # await weather_coordinator.async_refresh()
    await weather_coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        ENTRY_NAME: name,
        ENTRY_WEATHER_COORDINATOR: weather_coordinator,
        CONF_CITY: city,
        CONF_LANGUAGE: language,
        CONF_MODE: forecast_mode,
        CONF_IMAGES_PATH: images_path,
        CONF_UPDATE_INTERVAL: ims_scan_Int,
    }

    await hass.config_entries.async_forward_entry_setup(entry, Platform.WEATHER)

    update_listener = entry.add_update_listener(async_update_options)
    hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER] = update_listener
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, Platform.WEATHER
    )

    _LOGGER.info("Unloading IMS Weather")

    if unload_ok:
        update_listener = hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER]
        update_listener()

        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def _get_config_value(config_entry: ConfigEntry, key: str) -> Any:
    if config_entry.options:
        return config_entry.options[key]
    return config_entry.data[key]


def _filter_domain_configs(elements, domain):
    return list(filter(lambda elem: elem["platform"] == domain, elements))
