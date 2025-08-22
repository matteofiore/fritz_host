from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

async def async_setup_entry(hass, entry, async_add_entities):
    host = entry.data["host"]
    user = entry.data["username"]
    password = entry.data["password"]

    fc = FritzConnection(address=host, user=user, password=password)
    hosts = FritzHosts(fc)
    async_add_entities([FritzActiveHostsSensor(hosts)])

class FritzActiveHostsSensor(SensorEntity):
    def __init__(self, hosts):
        self._hosts = hosts
        self._state = None
        self._name = "Fritz Active Hosts"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        self._state = len(self._hosts.get_active_hosts())
