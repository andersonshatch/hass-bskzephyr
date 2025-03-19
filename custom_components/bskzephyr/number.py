from homeassistant.const import PERCENTAGE
from . import BSKZephyrConfigEntry, BSKDataUpdateCoordinator
from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

NUMBER_TYPES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        name="Humidity Boost",
        key="humidityBoost",
        min_value=0,
        max_value=100,
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:water-percent",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: BSKZephyrConfigEntry, async_add_entities
) -> None:
    for groupID, device in entry.runtime_data.coordinator.data.items():
        async_add_entities(
            BSKZephyrNumber(groupID, entry.runtime_data.coordinator, description)
            for description in NUMBER_TYPES
        )


class BSKZephyrNumber(NumberEntity, CoordinatorEntity[BSKDataUpdateCoordinator]):
    def __init__(
        self,
        groupID: str,
        coordinator: BSKDataUpdateCoordinator,
        description: NumberEntityDescription,
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

        if description.min_value is not None:
            self._attr_min_value = description.min_value

        if description.max_value is not None:
            self._attr_native_max_value = description.max_value

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )
        self._handle_coordinator_update()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = getattr(
            self.coordinator.data[self.groupID].device, self.entity_description.key
        )
        self.async_write_ha_state()

    async def async_set_native_value(self, value):
        self._attr_native_value = value
        await self.coordinator.api.control_device(
            self.groupID, **{self.entity_description.key: value}
        )
        await self.coordinator.async_request_refresh()
