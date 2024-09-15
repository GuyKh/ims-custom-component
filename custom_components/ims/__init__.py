import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_MODE,
    CONF_NAME, CONF_MONITORED_CONDITIONS,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CITY,
    CONF_LANGUAGE,
    CONF_IMAGES_PATH,
    CONF_UPDATE_INTERVAL,
    DOMAIN,
    ENTRY_NAME,
    ENTRY_WEATHER_COORDINATOR,
    UPDATE_LISTENER,
    PLATFORMS,
    IMS_PLATFORMS,
    IMS_PLATFORM,
    DEFAULT_LANGUAGE,
    FORECAST_MODE_HOURLY,
)

from .weather_update_coordinator import WeatherUpdateCoordinator

CONF_FORECAST = "forecast"
CONF_HOURLY_FORECAST = "hourly_forecast"

_LOGGER = logging.getLogger(__name__)
ATTRIBUTION = "Powered by IMS Weather"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up IMS Weather as config entry."""
    name = entry.data[CONF_NAME]
    city = _get_config_value(entry, CONF_CITY)
    forecast_mode = _get_config_value(entry, CONF_MODE, FORECAST_MODE_HOURLY)
    images_path = _get_config_value(entry, CONF_IMAGES_PATH)
    language = _get_config_value(entry, CONF_LANGUAGE, DEFAULT_LANGUAGE)
    ims_entity_platform = _get_config_value(entry, IMS_PLATFORM)
    ims_scan_int = entry.data[CONF_UPDATE_INTERVAL]
    conditions = _get_config_value(entry, CONF_MONITORED_CONDITIONS)


    # Extract list of int from forecast days/ hours string if present
    # _LOGGER.warning('forecast_days_type: ' + str(type(forecast_days)))
    is_legacy_city = False
    if isinstance(city, int | str):
        is_legacy_city = True

    city_id = city if is_legacy_city else city['lid']

    unique_location = f"ims-{language}-{city_id}"

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
            city_id, language, timedelta(minutes=ims_scan_int), hass
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
        CONF_UPDATE_INTERVAL: ims_scan_int,
        IMS_PLATFORM: ims_entity_platform,
        CONF_MONITORED_CONDITIONS: conditions,
    }

    # If both platforms
    if (IMS_PLATFORMS[0] in ims_entity_platform) and (
            IMS_PLATFORMS[1] in ims_entity_platform
    ):
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # If only sensor
    elif IMS_PLATFORMS[0] in ims_entity_platform:
        await hass.config_entries.async_forward_entry_setups(entry, [PLATFORMS[0], PLATFORMS[2]])
    # If only weather
    elif IMS_PLATFORMS[1] in ims_entity_platform:
        await hass.config_entries.async_forward_entry_setup(entry, [PLATFORMS[1]])

    update_listener = entry.add_update_listener(async_update_options)
    hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER] = update_listener
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    ims_entity_prevplatform = hass.data[DOMAIN][entry.entry_id][IMS_PLATFORM]

    unload_ok = False
    # If both
    if (IMS_PLATFORMS[0] in ims_entity_prevplatform) and (
            IMS_PLATFORMS[1] in ims_entity_prevplatform
    ):
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    # If only sensor
    elif IMS_PLATFORMS[0] in ims_entity_prevplatform:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, [PLATFORMS[0], PLATFORMS[2]]
        )
    # If only Weather
    elif IMS_PLATFORMS[1] in ims_entity_prevplatform:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, [PLATFORMS[1]]
        )

    _LOGGER.info(f"Unloading IMS Weather. Successful: {unload_ok}")

    if unload_ok:
        update_listener = hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER]
        update_listener()

        hass.data[DOMAIN].pop(entry.entry_id)

    return True


def _get_config_value(config_entry: ConfigEntry, key: str, default = None) -> Any:
    if config_entry.options:
        val = config_entry.options.get(key)
        if val:
            return val
        else:
            _LOGGER.warning("Key %s is missing from config_entry.options", key)
            return default
    val = config_entry.data.get(key)
    if val:
        return val
    else:
        _LOGGER.warning("Key %s is missing from config_entry.data", key)
        return default



def _filter_domain_configs(elements, domain):
    return list(filter(lambda elem: elem["platform"] == domain, elements))


@dataclass(kw_only=True, frozen=True)
class ImsSensorEntityDescription(SensorEntityDescription):
    """Describes IMS Weather sensor entity."""
    field_name: str | None = None
    forecast_mode: str | None = None


class ImsEntity(CoordinatorEntity):
    """Define a generic Ims entity."""

    _attr_has_entity_name = True

    def __init__(
            self, coordinator: WeatherUpdateCoordinator, description: ImsSensorEntityDescription
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)

        self._attr_extra_state_attributes = {}
        self._attr_unique_id = (
            f"{description.key}_{coordinator.city}_{coordinator.language}"
        )

        self.entity_id = "sensor." + description.key
        self._attr_translation_key = f"{description.key}_{coordinator.language}"
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Respond to a DataUpdateCoordinator update."""
        self._update_from_latest_data()
        self.async_write_ha_state()

    @callback
    def _update_from_latest_data(self) -> None:
        """Update the entity from the latest data."""
        raise NotImplementedError

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        self._update_from_latest_data()
