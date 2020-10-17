"""The Recteq integration."""

import logging
import pytuya
import async_timeout

from datetime import timedelta
from time import time
from threading import Lock

from .const import (
    CONF_DEVICE_ID,
    CONF_FORCE_FAHRENHEIT,
    CONF_IP_ADDRESS,
    CONF_LOCAL_KEY,
    CONF_NAME,
    CONF_PROTOCOL,
    DOMAIN,
    DPS_POWER,
)

from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
    STATE_UNAVAILABLE,
    TEMP_FAHRENHEIT,
)
from homeassistant.helpers import update_coordinator

_LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 3
CACHE_SECONDS = 5
UPDATE_INTERVAL = timedelta(seconds=CACHE_SECONDS*2)

class RecteqDevice(update_coordinator.DataUpdateCoordinator):

    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER,
            name = entry.data[CONF_NAME],
            update_interval = UPDATE_INTERVAL,
        )

        self._device_id        = entry.data[CONF_DEVICE_ID]
        self._ip_address       = entry.data[CONF_IP_ADDRESS]
        self._local_key        = entry.data[CONF_LOCAL_KEY]
        self._protocol         = entry.data[CONF_PROTOCOL]
        self._force_fahrenheit = entry.options.get(CONF_FORCE_FAHRENHEIT, False)
        _LOGGER.debug("force_fahrenheit is {}".format(self._force_fahrenheit))

        self._pytuya = pytuya.OutletDevice(self._device_id, self._ip_address, self._local_key)
        self._pytuya.set_version(float(self._protocol))

        self._cached_status = None
        self._cached_status_time = None

        self._units = hass.config.units

        self._lock = Lock()

        self._unsub = entry.add_update_listener(async_update_listener)

    def __del__(self):
        self._unsub()

    @property
    def device_id(self):
        return self._device_id

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def local_key(self):
        return self._local_key

    @property
    def force_fahrenheit(self):
        return self._force_fahrenheit

    @property
    def available(self):
        return self._cached_status != None

    @property
    def is_on(self):
        return self.dps(DPS_POWER)

    @property
    def is_off(self):
        return not self.is_on

    def dps(self, dps, value = None):
        if value == None:
            if self._cached_status == None:
                return None
            value = self._cached_status[dps]
            return value
        else:
            _LOGGER.debug('set {}={}'.format(int(dps), value))
            return self._pytuya.set_status(value, dps)

    @property
    def units(self):
        return self._units

    @property
    def temperature_unit(self):
        if self._force_fahrenheit:
            return TEMP_FAHRENHEIT
        return self.units.temperature_unit

    def temperature(self, degrees_f):
        if self._force_fahrenheit:
            return degrees_f
        return self.units.temperature(degrees_f, TEMP_FAHRENHEIT)

    def update(self):
        self._lock.acquire()
        try:
            now = time()
            if not self._cached_status or now - self._cached_status_time > CACHE_SECONDS:
                retries = MAX_RETRIES
                while retries:
                    retries -= 1
                    try:
                        self._cached_status = self._pytuya.status()['dps']
                        self._cached_status_time = time()
                        _LOGGER.debug("update {}".format(self._cached_status))
                        return
                    except ConnectionError as err:
                        if retries <= 0:
                            self._cached_status = None
                            self._cached_status_time = time()
                            raise err
        finally:
            self._lock.release()

    async def async_update(self):
        await self.hass.async_add_executor_job(self.update)

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(5):
                await self.async_update()
        except ConnectionError as err:
            raise update_coordinator.UpdateFailed("Error fetching data") from err

async def async_update_listener(hass, entry):
    device = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("update entry: data={} options={}".format(entry.data, entry.options))
    device._force_fahrenheit = entry.options.get(CONF_FORCE_FAHRENHEIT, False)
    _LOGGER.debug("force_fahrenheit now {}".format(device.force_fahrenheit))
