"""Fritz!Box Host Sensor integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "fritz_hosts"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration from configuration.yaml (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config flow entry."""
    # Qui puoi salvare l'IP, utente e password
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    # Creazione del sensore
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True
