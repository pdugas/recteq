"""The Recteq integration."""

import logging
import pytuya
import async_timeout

from datetime import timedelta
from time import time
from threading import Lock

from .const import DOMAIN, CONF_NAME, DPS_POWER

from homeassistant.const import EVENT_HOMEASSISTANT_STOP, STATE_UNAVAILABLE
from homeassistant.helpers import update_coordinator

_LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 3
CACHE_SECONDS = 5
UPDATE_INTERVAL = timedelta(seconds=CACHE_SECONDS*2)

class RecteqDevice(update_coordinator.DataUpdateCoordinator):

    def __init__(self, hass, entry, device_id, ip_address, local_key, protocol):
        super().__init__(hass, _LOGGER,
            name = entry.data[CONF_NAME],
            update_interval = UPDATE_INTERVAL,
        )
        self._device_id  = device_id
        self._ip_address = ip_address
        self._local_key  = local_key
        self._protocol   = protocol
        self._pytuya = pytuya.OutletDevice(device_id, ip_address, local_key)
        self._pytuya.set_version(float(protocol))
        self._cached_status = None
        self._cached_status_time = None
        self._lock = Lock()

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
            _LOGGER.debug('Read {} value; {}={}'.format(self.name, dps, value))
            return value
        else:
            _LOGGER.debug('Write {} value; {}={}'.format(self.name, dps, value))
            #self._cached_status[dps] = value
            return self._pytuya.set_status(value, dps)

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
