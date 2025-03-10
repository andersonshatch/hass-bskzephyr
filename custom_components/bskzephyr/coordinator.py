"""DataUpdateCoordinator for BSK Zephyr."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Dict, List

from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from bskzephyr import BSKZephyrClient, Zephyr, ZephyrException

#from . import BSKZephyrConfigEntry
from .const import DOMAIN, SUPPORTED_MODELS

_LOGGER = logging.getLogger(__name__)


class DeviceDataUpdateCoordinator(DataUpdateCoordinator[List[Zephyr]]):
    """BSK Zephyr Data Update Coordinator."""

    config_entry: BSKZephyrConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: BSKZephyrConfigEntry, client: BSKZephyrClient
    ) -> None:
        """Initialize data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=f"{DOMAIN}_{config_entry.data[CONF_USERNAME]}",
            update_interval=timedelta(minutes=2),
            always_update=False
        )

        self.data = {}
        self.api = client

    async def _async_update_data(self) -> Dict[str: Zephyr]:
        """Request to the server to update the status from full response data."""
        try:
            device_list = await self.api.list_devices()
            return {device.device.groupID: device for device in device_list if device.deviceModel in SUPPORTED_MODELS}
        except ZephyrException as e:
            raise UpdateFailed(e) from e

    # def refresh_status(self) -> None:
    #     """Refresh current status."""
    #     self.async_set_updated_data(self.data)


async def async_setup_device_coordinator(
    hass: HomeAssistant, config_entry: BSKZephyrConfigEntry, client: BSKZephyrClient
) -> DeviceDataUpdateCoordinator:
    """Create DeviceDataUpdateCoordinator and device_api per device."""
    coordinator = DeviceDataUpdateCoordinator(hass, config_entry, client)
    await coordinator.async_refresh()

    _LOGGER.debug(
        "Setup device's coordinator",
    )
    return coordinator