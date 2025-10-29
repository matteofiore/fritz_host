"""Config flow for Fritz!Box Hosts integration."""

from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from fritzconnection import FritzConnection
from .const import DOMAIN
import functools


async def validate_input(hass: HomeAssistant, data: dict):
    """Validate the user input by testing the Fritz!Box connection."""
    def _test_connection():
        fc = FritzConnection(
            address=data["host"],
            user=data["username"],
            password=data["password"]
        )
        # Proviamo una chiamata base per verificare che il dispositivo risponda
        fc.call_action("WANIPConnection:1", "GetStatusInfo")

    await hass.async_add_executor_job(_test_connection)


class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fritz!Box Hosts."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
                return self.async_create_entry(
                    title="Fritz!Box Hosts",
                    data=user_input,
                )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required("host", default="192.168.178.1"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Optional("update_interval", default=60): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
