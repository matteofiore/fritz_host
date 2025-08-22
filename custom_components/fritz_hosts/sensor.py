"""Fritz!Box host sensor."""

from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts
import functools

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor from config flow entry."""
    config = entry.data
    host_data = {
        "address": config["host"],
        "username": config["username"],
        "password": config["password"]
    }

    # Crea il sensore e aggiungilo
    async_add_entities([FritzHostsSensor(hass, host_data)])


class FritzHostsSensor(SensorEntity):
    """Representation of a Fritz!Box hosts sensor."""

    def __init__(self, hass, host_data):
        self.hass = hass
        self._host_data = host_data
        self._attr_name = "Fritz!Box Active Hosts"
        self._attr_native_value = None

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        """Aggiorna lo stato del sensore senza bloccare Home Assistant."""
        # Crea la connessione in un thread separato
        fc = await self.hass.async_add_executor_job(
            functools.partial(
                FritzConnection,
                address=self._host_data["address"],
                user=self._host_data["username"],
                password=self._host_data["password"]
            )
        )

        # Ottieni i dispositivi attivi in un thread separato
        active_hosts = await self.hass.async_add_executor_job(
            functools.partial(lambda fc: FritzHosts(fc).get_active_hosts(), fc)
        )

        self._attr_native_value = len(active_hosts)
