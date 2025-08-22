"""Config flow for Fritz!Box Host Sensor integration."""
from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class FritzHostsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FritzHosts."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Fritz!Box", data=user_input)

        data_schema = vol.Schema({
            vol.Required("address", default="192.168.1.1"): str,
            vol.Required("user"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)
