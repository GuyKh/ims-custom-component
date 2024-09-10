from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntityDescription, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_MONITORED_CONDITIONS
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ImsEntity, ImsSensorEntityDescription
from .const import (TYPE_IS_RAINING, IMS_SENSOR_KEY_PREFIX, FORECAST_MODE, FIELD_NAME_RAIN, DOMAIN,
                    ENTRY_WEATHER_COORDINATOR)
from .weather_update_coordinator import WeatherData



@dataclass(frozen=True, kw_only=True)
class ImsBinaryEntityDescriptionMixin:
    """Mixin values for required keys."""

    value_fn: Callable[[WeatherData], bool | None]


@dataclass(frozen=True, kw_only=True)
class ImsBinarySensorEntityDescription(ImsSensorEntityDescription, BinarySensorEntityDescription, ImsBinaryEntityDescriptionMixin):
    """Class describing IMS Binary sensors entities"""


BINARY_SENSORS_DESCRIPTIONS: tuple[ImsBinarySensorEntityDescription, ...] = (
    ImsBinarySensorEntityDescription(
        key=IMS_SENSOR_KEY_PREFIX + TYPE_IS_RAINING,
        name="IMS Is Raining",
        icon="mdi:weather-rainy",
        forecast_mode=FORECAST_MODE.CURRENT,
        field_name=FIELD_NAME_RAIN,
        value_fn=lambda data: data.current_weather.rain and data.current_weather.rain > 0.0
    ),
)

BINARY_SENSOR_DESCRIPTIONS_DICT = {desc.key: desc for desc in BINARY_SENSORS_DESCRIPTIONS}
BINARY_SENSOR_DESCRIPTIONS_KEYS = [desc.key for desc in BINARY_SENSORS_DESCRIPTIONS]

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a IMS binary sensors based on a config entry."""
    domain_data = hass.data[DOMAIN][entry.entry_id]
    conditions = domain_data[CONF_MONITORED_CONDITIONS]
    weather_coordinator = domain_data[ENTRY_WEATHER_COORDINATOR]

    # Add IMS Sensors
    sensors: list[ImsBinarySensor] = []

    if conditions is None:
        # If a problem happens - create all sensors
        conditions = BINARY_SENSOR_DESCRIPTIONS_KEYS

    for condition in conditions:
        if condition in BINARY_SENSOR_DESCRIPTIONS_KEYS:
            description = BINARY_SENSOR_DESCRIPTIONS_DICT[condition]
            sensors.append(ImsBinarySensor(weather_coordinator, description))


    async_add_entities(sensors, update_before_add=True)

class ImsBinarySensor(ImsEntity, BinarySensorEntity):
    """Defines an IMS binary sensor."""

    @callback
    def _update_from_latest_data(self) -> None:
        """Update the state."""
        self._attr_is_on = self.entity_description.value_fn(self.coordinator.data)
