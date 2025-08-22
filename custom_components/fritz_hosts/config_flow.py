import asyncio
import functools
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts


class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fritz!Box Hosts."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Esegui la connessione e la chiamata sincrona in un executor
                fc = await self.hass.async_add_executor_job(
                    functools.partial(
                        FritzConnection,
                        address=user_input["host"],
                        user=user_input["username"],
                        password=user_input["password"]
                    )
                )

                active_hosts = await self.hass.async_add_executor_job(
                    functools.partial(
                        lambda fc: FritzHosts(fc).get_active_hosts(),
                        fc
                    )
                )

                # Se la connessione funziona, crea la configurazione
                return self.async_create_entry(
                    title=f"Fritz!Box {user_input['host']}",
                    data=user_input
                )

            except Exception as e:
                errors["base"] = "cannot_connect"
                self._async_handle_exception(e)

        # Form di input
        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
