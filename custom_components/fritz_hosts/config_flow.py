import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "fritz_hosts"

class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fritz!Box Host Sensor."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Qui puoi validare host, username e password
            return self.async_create_entry(title="Fritz!Box", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host", default="192.168.1.1"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
