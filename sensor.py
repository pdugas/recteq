"""The Recteq sensor component."""

from .const import (
    DOMAIN,
    DPS_PROBEA,
    DPS_PROBEB
)

from homeassistant.components.sensor import DEVICE_CLASS_TEMPERATURE
from homeassistant.const import TEMP_FAHRENHEIT, STATE_UNAVAILABLE
from homeassistant.core import callback
from homeassistant.helpers import entity

async def async_setup_entry(hass, entry, add):
    device = hass.data[DOMAIN][entry.entry_id]
    add(
        [
            RecteqSensor(device, DPS_PROBEA, 'Probe A Temperature'),
            RecteqSensor(device, DPS_PROBEB, 'Probe B Temperature')
        ]
    )

class RecteqSensor(entity.Entity):

    def __init__(self, device, dps, name):
        self._device = device
        self._dps = dps
        self._name = f"{device.name} {name}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self):
        return f"{self._device.device_id}.{self._dps}"

    @property
    def available(self):
        return self._device.available and self._device.is_on

    @property
    def state(self):
        if self.available:
            value = self._device.dps(self._dps)
            if value == None:
                return None
            return round(float(value))
        return STATE_UNAVAILABLE

    @property
    def unit_of_measurement(self):
        return TEMP_FAHRENHEIT

    @property
    def device_class(self):
        return DEVICE_CLASS_TEMPERATURE

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self._device.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(self._device.async_add_listener(self._update_callback))

    @callback
    def _update_callback(self):
        self.async_write_ha_state()
