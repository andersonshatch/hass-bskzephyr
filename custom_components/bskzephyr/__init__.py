"""The BSK Zephyr integration."""

from __future__ import annotations
from dataclasses import dataclass

from .coordinator import DeviceDataUpdateCoordinator, async_setup_device_coordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from bskzephyr import BSKZephyrClient, InvalidAuthError
from homeassistant.exceptions import ConfigEntryAuthFailed

_PLATFORMS: list[Platform] = [
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


@dataclass(kw_only=True)
class BSKZephyrData:
    coordinator: DeviceDataUpdateCoordinator


type BSKZephyrConfigEntry = ConfigEntry[BSKZephyrData]  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: BSKZephyrConfigEntry) -> bool:
    """Set up BSK Zephyr from a config entry."""

    client = BSKZephyrClient(
        async_get_clientsession(hass),
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
    )

    try:
        await client.login()
    except InvalidAuthError as err:
        raise ConfigEntryAuthFailed("Credentials error from BSK Zephyr") from err

    coordinator = await hass.async_create_task(
        async_setup_device_coordinator(hass, entry, client)
    )
    entry.runtime_data = BSKZephyrData(coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: BSKZephyrConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
