"""The Recteq climate component."""

import logging

from .const import (
    DOMAIN,
    DPS_ACTUAL,
    DPS_POWER,
    DPS_TARGET,
    POWER_OFF,
    POWER_ON,
)
from .device import RecteqDevice

from homeassistant.components import climate
from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
    ATTR_CURRENT_TEMPERATURE
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    TEMP_FAHRENHEIT,
    STATE_UNAVAILABLE
)
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

ICON = 'mdi:grill'

TEMP_MIN = 200
TEMP_MAX = 500

# TODO Support "Max Smoke" Mode
#   The recteq app sets the target temperature to this value when it's on
#   TEMP_MIN and the user taps the "-" button one more time.
TEMP_SMOKE = 180

# TODO Support "Full" Mode
#   The recteq app sets the target temperature to this value when it's on
#   TEMP_MAX and the user taps the "+" button one more time.
TEMP_FULL  = 600

async def async_setup_entry(hass, entry, add):
    add([RecteqClimate(hass.data[DOMAIN][entry.entry_id])])

class RecteqClimate(climate.ClimateEntity):

    def __init__(self, device: RecteqDevice):
        super().__init__()
        self._device    = device

    @property
    def name(self):
        return self._device.name

    @property
    def unique_id(self):
        return self._device.device_id

    @property
    def icon(self):
        return ICON

    @property
    def available(self):
        return self._device.available

    @property
    def precision(self):
        return PRECISION_WHOLE

    @property
    def temperature_unit(self):
        return TEMP_FAHRENHEIT

    @property
    def is_on(self):
        return self._device.is_on

    @property
    def is_off(self):
        return self._device.is_off

    @property
    def hvac_mode(self):
        if self.is_on:
            return HVAC_MODE_HEAT

        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT]

    @property
    def current_temperature(self):
        temp = self._device.dps(DPS_ACTUAL)
        if temp == None:
            return None
        return float(temp)

    @property
    def target_temperature(self):
        temp = self._device.dps(DPS_TARGET)
        if temp == None:
            return None
        return float(temp)

    @property
    def target_temperature_step(self):
        return 5.0

    @property
    def target_temperature_high(self):
        return self.max_temp

    @property
    def target_temperature_low(self):
        return self.min_temp

    def set_temperature(self, **kwargs):
        mode = kwargs.get(ATTR_HVAC_MODE)
        if mode != None:
            self.set_hvac_mode(mode)

        temp = kwargs.get(ATTR_TEMPERATURE)
        self._device.dps(DPS_TARGET, int(temp))

    def set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVAC_MODE_HEAT:
            self.turn_on()
        elif hvac_mode == HVAC_MODE_OFF:
            self.turn_off()
        else:
            raise Exception('Invalid hvac_mode; "{}"'.format(hvac_mode))
            
    @property
    def is_on(self):
        return self._device.dps(DPS_POWER) == POWER_ON

    @property
    def is_off(self):
        return not self.is_on

    def turn_on(self):
        self.set_hvac_mode(HVAC_MODE_HEAT)

    def turn_off(self):
        self.set_hvac_mode(HVAC_MODE_OFF)

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def min_temp(self):
        return TEMP_MIN

    @property
    def max_temp(self):
        return TEMP_MAX

    @property
    def state_attributes(self):
        data = { ATTR_TEMPERATURE: round(self._device.dps(DPS_TARGET)) }
        if self.is_on:
            data[ATTR_CURRENT_TEMPERATURE] = round(self._device.dps(DPS_ACTUAL))
        else:
            data[ATTR_CURRENT_TEMPERATURE] = STATE_UNAVAILABLE
        return data

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
