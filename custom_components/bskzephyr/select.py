from . import BSKZephyrConfigEntry, DeviceDataUpdateCoordinator
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from bskzephyr import FanMode, FanSpeed

SELECT_TYPES: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        name="Fan Mode", key="fanMode", options=[m.value for m in FanMode]
    ),
    SelectEntityDescription(
        name="Fan Speed", key="fanSpeed", options=[s.name for s in FanSpeed]
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: BSKZephyrConfigEntry, async_add_entities
) -> None:
    for groupID, device in entry.runtime_data.coordinator.data.items():
        async_add_entities(
            BSKZephyrSelect(groupID, entry.runtime_data.coordinator, description)
            for description in SELECT_TYPES
        )


class BSKZephyrSelect(SelectEntity, CoordinatorEntity[DeviceDataUpdateCoordinator]):
    def __init__(
        self,
        groupID: str,
        coordinator: DeviceDataUpdateCoordinator,
        description: SelectEntityDescription,
    ):
        super().__init__(coordinator)

        self._attr_unique_id = f"{groupID}-{description.key}"
        self._attr_name = f"{coordinator.data[groupID].groupTitle} {description.name}"
        self._attr_device_info = DeviceInfo(
            connections={(CONNECTION_NETWORK_MAC, groupID)},
            name=coordinator.data[groupID].groupTitle,
            model=coordinator.data[groupID].deviceModel,
            sw_version=coordinator.data[groupID].device.version,
        )
        self.coordinator = coordinator
        self.groupID = groupID
        self.entity_description = description

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )
        self._handle_coordinator_update()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_state = getattr(
            self.coordinator.data[self.groupID].device, self.entity_description.key
        )
        self.async_write_ha_state()

    @property
    def state(self):
        return self._attr_state.name

    async def async_select_option(self, option: str) -> None:
        self._attr_state = (self._attr_state.__class__)[option]

        await self.coordinator.api.control_device(
            self.groupID, **{self.entity_description.key: self._attr_state}
        )
        await self.coordinator.async_request_refresh()

        # setattr(self.coordinator.data[self.deviceID].settings, self.entity_description.key, self._attr_state)
        # self.coordinator.data[self.deviceID].settings.deviceID = self.deviceID
        # self.coordinator.data[self.deviceID].settings.groupID = self.coordinator.data[self.deviceID].groupID
        # print(dict(self.coordinator.data[self.deviceID].settings))
        # await self.coordinator.api.update_group_settings(dict(self.coordinator.data[self.deviceID].settings))
