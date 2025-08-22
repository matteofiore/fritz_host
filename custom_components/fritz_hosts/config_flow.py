"""Fritz!Box host sensor."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import DEVICE_CLASS_MONITOR
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
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
        "password": config["password"],
        "update_interval": config.get("update_interval", 60)  # default 60 secondi
    }

    sensor = FritzHostsSensor(hass, host_data)
    async_add_entities([sensor], True)


class FritzHostsSensor(SensorEntity):
    """Representation of a Fritz!Box hosts sensor."""

    def __init__(self, hass, host_data):
        self.hass = hass
        self._host_data = host_data
        self._attr_name = "Fritz!Box Active Hosts"
        self._attr_native_value = None
        self._attr_device_class = DEVICE_CLASS_MONITOR
        self._attr_state_class = "measurement"
        self._attr_unique_id = f"fritz_hosts_{host_data['address']}"

        self._unsub_update = None  # memorizza il listener dell'update periodico

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        """Aggiorna il sensore senza bloccare Home Assistant."""
        fc = await self.hass.async_add_executor_job(
            functools.partial(
                FritzConnection,
                address=self._host_data["address"],
                user=self._host_data["username"],
                password=self._host_data["password"]
            )
        )

        active_hosts = await self.hass.async_add_executor_job(
            functools.partial(lambda fc: FritzHosts(fc).get_active_hosts(), fc)
        )

        self._attr_native_value = len(active_hosts)

    async def async_added_to_hass(self):
        """Quando il sensore viene aggiunto, avvia l'update periodico."""
        interval = timedelta(seconds=self._host_data.get("update_interval", 60))
        self._unsub_update = async_track_time_interval(
            self.hass, lambda now: self.async_update(), interval
        )

    async def async_will_remove_from_hass(self):
        """Annulla l'update periodico quando il sensore viene rimosso."""
        if self._unsub_update:
            self._unsub_update()
            self._unsub_update = None
