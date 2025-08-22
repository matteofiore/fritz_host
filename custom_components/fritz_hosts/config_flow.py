import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required("host"): str,
    vol.Required("username"): str,
    vol.Required("password"): str,
})

class FritzHostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input["host"]
            username = user_input["username"]
            password = user_input["password"]
            
            # qui puoi fare un test di connessione
            try:
                from fritzconnection import FritzConnection
                fc = FritzConnection(address=host, user=username, password=password)
                fc.get_ftp_hosts = fc.call_action('Hosts1', 'GetHostList')
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(title="Fritz Host", data=user_input)

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
