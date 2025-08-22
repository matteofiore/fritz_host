"""Fritz Hosts integration."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Fritz Hosts integration from configuration.yaml (if needed)."""
    # Non è richiesto se usi solo config flow
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Fritz Hosts from a config entry."""
    # Inoltra la configurazione al sensore
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
