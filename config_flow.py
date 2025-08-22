import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_HOST

DOMAIN = "fritz_hosts"

class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FritzHosts."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Salva la configurazione inserita dall’utente
            return self.async_create_entry(title="FritzBox Hosts", data=user_input)

        # Mostra il form per inserire IP, utente e password
        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default="192.168.1.1"): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })
        return self.async_show_form(step_id="user", data_schema=data_schema)