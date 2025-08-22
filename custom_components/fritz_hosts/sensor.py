from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
)
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

_LOGGER = logging.getLogger(__name__)

DOMAIN = "fritz_hosts"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the FritzHosts sensor with periodic updates."""
    host = config_entry.data[CONF_HOST]
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]

    fc = FritzConnection(address=host, user=username, password=password)
    hosts = FritzHosts(fc)

    async def async_update_data():
        """Fetch active hosts from FritzBox."""
        return len(hosts.get_active_hosts())

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="fritz_hosts",
        update_method=async_update_data,
        update_interval=timedelta(minutes=1),  # aggiorna ogni minuto
    )

    # primo aggiornamento
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([FritzHostsCoordinatorSensor(coordinator)])


class FritzHostsCoordinatorSensor(CoordinatorEntity, SensorEntity):
    """FritzHosts sensor using DataUpdateCoordinator."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Fritz!Box Active Hosts"
        self._attr_unit_of_measurement = "devices"

    @property
    def native_value(self):
        return self.coordinator.data
