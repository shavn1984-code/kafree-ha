"""Config flow for Kafree."""
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import callback
from .const import CONF_BASE_URL, CONF_PHONE, CONF_SCAN_INTERVAL, CONF_SN, CONF_TOKEN, DEFAULT_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

class KafreeConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return await self.async_step_token()
        return self.async_show_form(step_id="user", errors={})

    async def async_step_token(self, user_input=None):
        errors = {}
        if user_input is not None:
            token = user_input.get(CONF_TOKEN, "").strip()
            base_url = user_input.get(CONF_BASE_URL, "").strip().rstrip("/") or DEFAULT_BASE_URL
            if not token:
                errors[CONF_TOKEN] = "token_required"
            else:
                await self.async_set_unique_id(f"kafree_{token[:8]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="咖啡自由",
                    data={CONF_TOKEN: token, CONF_BASE_URL: base_url},
                )
        return self.async_show_form(
            step_id="token",
            data_schema=vol.Schema({
                vol.Required(CONF_TOKEN): str,
                vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KafreeOptionsFlowHandler(config_entry)


class KafreeOptionsFlowHandler(OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        schema = {}
        schema[
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
        ] = vol.All(vol.Coerce(int), vol.Range(min=30, max=86400))
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
        )
