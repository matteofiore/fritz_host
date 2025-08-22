"""Fritz!Box host sensor."""

from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor from config flow entry."""
    config = entry.data
    fc = FritzConnection(
        address=config["address"],
        user=config["user"],
        password=config["password"]
    )
    hosts = FritzHosts(fc)
    active_hosts = hosts.get_active_hosts()
    
    async_add_entities([FritzHostsSensor(len(active_hosts))])

class FritzHostsSensor(SensorEntity):
    """Representation of a Fritz!Box hosts sensor."""

    def __init__(self, count):
        self._attr_name = "Fritz!Box Active Hosts"
        self._attr_native_value = count

    @property
    def native_value(self):
        return self._attr_native_value
