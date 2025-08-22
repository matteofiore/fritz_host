import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

import logging

_LOGGER = logging.getLogger(__name__)

class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FritzHosts."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Test connection
                fc = FritzConnection(
                    address=user_input["host"],
                    user=user_input["username"],
                    password=user_input["password"]
                )
                hosts = FritzHosts(fc)
                active_hosts = hosts.get_active_hosts()
                _LOGGER.info("Totale dispositivi attivi: %s", len(active_hosts))

                return self.async_create_entry(
                    title=f"{user_input['host']} ({len(active_hosts)} hosts)",
                    data=user_input
                )

            except Exception as e:
                _LOGGER.error("Errore connessione FritzBox: %s", e)
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
