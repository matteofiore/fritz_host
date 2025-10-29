"""Fritz!Box host sensor."""

from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts
import functools
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor from config flow entry."""
    config = entry.data
    host_data = {
        "address": config["host"],
        "username": config["username"],
        "password": config["password"],
        "update_interval": config.get("update_interval", 60),  # default: 60 secondi
    }

    sensor = FritzHostsSensor(hass, host_data)
    async_add_entities([sensor], True)


class FritzHostsSensor(SensorEntity):
    """Representation of a Fritz!Box hosts sensor."""

    _attr_name = "Fritz!Box Active Hosts"
    _attr_icon = "mdi:router-network"
    _attr_native_unit_of_measurement = "hosts"

    def __init__(self, hass, host_data):
        self.hass = hass
        self._host_data = host_data
        self._attr_native_value = None
        self._attr_unique_id = f"fritz_hosts_{host_data['address']}"
        self._unsub_update = None  # listener per l'update periodico

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_update(self):
        """Aggiorna lo stato del sensore senza bloccare Home Assistant."""
        try:
            fc = await self.hass.async_add_executor_job(
                functools.partial(
                    FritzConnection,
                    address=self._host_data["address"],
                    user=self._host_data["username"],
                    password=self._host_data["password"],
                )
            )

            active_hosts = await self.hass.async_add_executor_job(
                lambda: FritzHosts(fc).get_active_hosts()
            )

            self._attr_native_value = len(active_hosts)

        except Exception as e:
            _LOGGER.warning(f"Errore durante l'aggiornamento Fritz!Box: {e}")
            self._attr_native_value = None

    async def async_added_to_hass(self):
        """Quando il sensore viene aggiunto, avvia l'aggiornamento periodico."""
        interval = timedelta(seconds=self._host_data["update_interval"])

        async def _update(now):
            await self.async_update()
            self.async_write_ha_state()

        # Avvia il timer periodico
        self._unsub_update = async_track_time_interval(self.hass, _update, interval)

        # Aggiorna subito alla creazione
        await self.async_update()
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self):
        """Ferma il timer quando il sensore viene rimosso."""
        if self._unsub_update:
            self._unsub_update()
            self._unsub_update = None
