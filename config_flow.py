from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
import voluptuous as vol
from .const import DOMAIN, SCAN_INTERVAL
from .wdmycloud import MyCloudClient
import logging
from typing import Any, Dict, Optional

_LOGGER = logging.getLogger(__name__)

class WDMyCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WD MyCloud."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                client = MyCloudClient(user_input[CONF_HOST])
                success = await self.hass.async_add_executor_job(
                    client.login,
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD]
                )

                if success:
                    return self.async_create_entry(
                        title=f"WD MyCloud ({user_input[CONF_HOST]})",
                        data=user_input
                    )
                else:
                    errors["base"] = "invalid_auth"
            except Exception as ex:
                _LOGGER.error("Connection failed: %s", str(ex))
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return WDMyCloudOptionsFlow(config_entry)

class WDMyCloudOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "scan_interval",
                    default=self.config_entry.options.get(
                        "scan_interval", SCAN_INTERVAL
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300)),
            }),
        )
