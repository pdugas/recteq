"""Config flow for the Recteq integration."""

import asyncio
import socket
import string
import uuid
import voluptuous as vol

from .const import (
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_LOCAL_KEY,
    CONF_NAME,
    CONF_PROTOCOL,
    CONF_FORCE_FAHRENHEIT,
    DEFAULT_PROTOCOL,
    DOMAIN,
    LEN_DEVICE_ID,
    LEN_LOCAL_KEY,
    PROTOCOLS,
    STR_INVALID_PREFIX,
    STR_PLEASE_CORRECT,
)
from collections import OrderedDict
from homeassistant import config_entries

@config_entries.HANDLERS.register(DOMAIN)
class RecteqFlowHandler(config_entries.ConfigFlow):
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        self._errors = {}
        self._data = {}
        self._data["unique_id"] = str(uuid.uuid4())

    async def async_step_user(self, user_input=None):
        self._errors = {}

        if user_input is not None:
            self._data.update(user_input)

            try:
                socket.inet_aton(user_input[CONF_IP_ADDRESS])
            except socket.error:
                self._errors[CONF_IP_ADDRESS] = STR_INVALID_PREFIX + CONF_IP_ADDRESS

            user_input[CONF_DEVICE_ID] = user_input[CONF_DEVICE_ID].replace(" ", " ")
            if (len(user_input[CONF_DEVICE_ID]) != LEN_DEVICE_ID or
                    not all(c in string.hexdigits for c in user_input[CONF_DEVICE_ID])):
                self._errors[CONF_DEVICE_ID] = STR_INVALID_PREFIX + CONF_DEVICE_ID

            user_input[CONF_LOCAL_KEY] = user_input[CONF_LOCAL_KEY].replace(" ", " ")
            if (len(user_input[CONF_LOCAL_KEY]) != LEN_LOCAL_KEY or 
                    not all(c in string.hexdigits for c in user_input[CONF_LOCAL_KEY])):
                self._errors[CONF_LOCAL_KEY] = STR_INVALID_PREFIX + CONF_LOCAL_KEY

            user_input[CONF_PROTOCOL] = user_input[CONF_PROTOCOL].strip()
            if user_input[CONF_PROTOCOL] not in PROTOCOLS:
                self._errors[CONF_PROTOCOL] = STR_INVALID_PREFIX + CONF_PROTOCOL

            if self._errors == {}:
                self.init_info = user_input
                return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)
            else:
                self._errors["base"] = STR_PLEASE_CORRECT

        return await self._show_user_form(user_input)

    async def _show_user_form(self, user_input):
        name             = ''
        ip_address       = ''
        device_id        = ''
        local_key        = ''
        protocol         = DEFAULT_PROTOCOL
        force_fahrenheit = False

        if user_input is not None:
            if CONF_NAME in user_input:
                name = user_input[CONF_NAME]
            if CONF_IP_ADDRESS in user_input:
                ip_address = user_input[CONF_IP_ADDRESS]
            if CONF_DEVICE_ID in user_input:
                device_id = user_input[CONF_DEVICE_ID]
            if CONF_LOCAL_KEY in user_input:
                local_key = user_input[CONF_LOCAL_KEY]
            if CONF_PROTOCOL in user_input:
                protocol = user_input[CONF_PROTOCOL]
            if CONF_FORCE_FAHRENHEIT in user_input:
                force_fahrenheit = user_input[CONF_FORCE_FAHRENHEIT]

        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_NAME,             default=name)]             = str
        data_schema[vol.Required(CONF_IP_ADDRESS,       default=ip_address)]       = str
        data_schema[vol.Required(CONF_DEVICE_ID,        default=device_id)]        = str
        data_schema[vol.Required(CONF_LOCAL_KEY,        default=local_key)]        = str
        data_schema[vol.Required(CONF_PROTOCOL,         default=protocol)]         = str
        data_schema[vol.Required(CONF_FORCE_FAHRENHEIT, default=force_fahrenheit)] = bool

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=self._errors
        )
