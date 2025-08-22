import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor from config flow entry."""
    ip = entry.data[CONF_HOST]
    user = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    async_add_entities([FritzHostsSensor(ip, user, password)])

class FritzHostsSensor(SensorEntity):
    """Sensor che mostra il numero di dispositivi FritzBox attivi."""

    def __init__(self, ip, user, password):
        self._state = None
        self._name = "FritzBox Active Hosts"
        self._ip = ip
        self._user = user
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "dispositivi"

    async def async_update(self):
        try:
            fc = FritzConnection(address=self._ip, user=self._user, password=self._password)
            hosts = FritzHosts(fc)
            active_hosts = hosts.get_active_hosts()
            self._state = len(active_hosts)
        except Exception as e:
            _LOGGER.error(f"Errore aggiornamento FritzHostsSensor: {e}")
            self._state = None