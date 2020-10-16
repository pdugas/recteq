"""Constants for the Recteq integration."""

import homeassistant.const as hac

PROJECT = 'Recteq Custom Integration'

VERSION_TUPLE = (0, 0, 3)
VERSION = __version__ = '%d.%d.%d' % VERSION_TUPLE

__author__ = 'Paul Dugas <paul@dugas.cc>'

ISSUE_LINK = 'https://github.com/pdugas/recteq/issues'

DOMAIN = 'recteq'

PLATFORMS = ['climate', 'sensor']

DPS_POWER  = '1'
DPS_TARGET = '102'
DPS_ACTUAL = '103'
DPS_PROBEA = '105'
DPS_PROBEB = '106'

ATTR_POWER  = 'power'   # read/write
ATTR_TARGET = 'target'  # read/write
ATTR_ACTUAL = 'actual'  # read-only
ATTR_PROBEA = 'probe_a' # read-only
ATTR_PROBEB = 'probe_b' # read-only

POWER_ON  = True
POWER_OFF = False

PROTOCOL_3_1 = '3.1'
PROTOCOL_3_3 = '3.3'

PROTOCOLS = [PROTOCOL_3_1, PROTOCOL_3_3]

LEN_DEVICE_ID = 20
LEN_LOCAL_KEY = 16

CONF_NAME             = hac.CONF_NAME
CONF_IP_ADDRESS       = hac.CONF_IP_ADDRESS
CONF_DEVICE_ID        = 'device_id'
CONF_LOCAL_KEY        = 'local_key'
CONF_PROTOCOL         = 'protocol'
CONF_FORCE_FAHRENHEIT = 'force_fahrenheit'

DEFAULT_PROTOCOL = PROTOCOL_3_3

STR_INVALID_PREFIX = 'invalid_'
STR_PLEASE_CORRECT = 'please_correct'

FORCE_FAHRENHEIT = True
