"""Config flow for Fritz Hosts integration."""
from homeassistant import config_entries
from .const import DOMAIN

class FritzHostsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Fritz Hosts."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Verifica credenziali qui, opzionale
            return self.async_create_entry(title="Fritz!Box", data=user_input)

        # Mostra il form iniziale
        return self.async_show_form(
            step_id="user",
            data_schema={
                "host": str,
                "username": str,
                "password": str,
            },
            errors=errors,
        )
