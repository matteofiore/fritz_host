import asyncio
import functools
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhosts import FritzHosts

class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gestione del flusso di configurazione per Fritz!Box Hosts."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step iniziale della configurazione."""
        errors = {}

        if user_input is not None:
            try:
                # Esegui la connessione in executor per non bloccare il loop
                fc = await self.hass.async_add_executor_job(
                    functools.partial(
                        FritzConnection,
                        address=user_input["host"],
                        user=user_input["username"],
                        password=user_input["password"]
                    )
                )

                # Leggi i dispositivi attivi sempre in executor
                active_hosts = await self.hass.async_add_executor_job(
                    functools.partial(lambda fc: FritzHosts(fc).get_active_hosts(), fc)
                )

                # Se tutto funziona, crea l’entry
                return self.async_create_entry(
                    title=f"Fritz!Box {user_input['host']}",
                    data=user_input
                )

            except Exception:
                errors["base"] = "cannot_connect"

        # Schema del form
        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Required("username"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
