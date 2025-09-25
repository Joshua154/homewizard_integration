import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .api import MyDeviceApiClient  # We will create this file next
from .const import DOMAIN


class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Device."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            try:
                # Use the handshake endpoint to validate the connection
                api_client = MyDeviceApiClient(host)
                await api_client.async_handshake()

                # If successful, create the config entry
                return self.async_create_entry(title=host, data=user_input)
            except Exception:
                # If handshake fails, show an error
                errors["base"] = "cannot_connect"

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )