"""Config flow for the BSK Zephyr integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from bskzephyr import BSKZephyrClient, InvalidAuthError, DEFAULT_SPEEDS, FanSpeed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional("speed_night", default=DEFAULT_SPEEDS[FanSpeed.night]): int,
        vol.Optional("speed_low", default=DEFAULT_SPEEDS[FanSpeed.low]): int,
        vol.Optional("speed_medium", default=DEFAULT_SPEEDS[FanSpeed.medium]): int,
        vol.Optional("speed_high", default=DEFAULT_SPEEDS[FanSpeed.high]): int,
    }
)


class SetupBSKZephyrConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BSK Zephyr."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME])
            self._abort_if_unique_id_configured()

            try:
                client = BSKZephyrClient(
                    async_get_clientsession(self.hass),
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                )
                await client.login()
            except InvalidAuthError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
