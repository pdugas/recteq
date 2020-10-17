"""The Recteq integration."""

import asyncio
import logging
import async_timeout

from .const import (
    DOMAIN,
    ISSUE_LINK,
    PLATFORMS,
    PROJECT,
    VERSION,
)

from .device import RecteqDevice

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE
from homeassistant.exceptions import ConfigEntryNotReady

from integrationhelper.const import CC_STARTUP_VERSION

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config):
    hass.data[DOMAIN] = {}

    _LOGGER.info(CC_STARTUP_VERSION.format(
        name=PROJECT,
        version=VERSION,
        issue_link=ISSUE_LINK
    ))

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN][entry.entry_id] = RecteqDevice(hass, entry)

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
                for PLATFORM in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

