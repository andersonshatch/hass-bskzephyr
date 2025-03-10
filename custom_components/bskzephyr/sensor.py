
import logging
from . import BSKZephyrConfigEntry
from .coordinator import DeviceDataUpdateCoordinator
from .entity import BSKZephyrEntity
from homeassistant.components.sensor import EntityCategory, SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo

from bskzephyr import Zephyr
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import SUPPORTED_MODELS

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        name="Temperature",
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1
    ),
    SensorEntityDescription(
        name="Humidity",
        key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1
    ),
    SensorEntityDescription(
         name="Filter Status",
         key="filterTimer",
         entity_category=EntityCategory.DIAGNOSTIC,
         icon="mdi:air-filter"
    ),
    SensorEntityDescription(
         name="Capsule Status",
         key="hygieneStatus",
         entity_category=EntityCategory.DIAGNOSTIC,
         icon="mdi:cylinder"
    ),
)


async def async_setup_entry(
        hass: HomeAssistant,
        entry: BSKZephyrConfigEntry,
        async_add_entities
    ) -> None:
        for groupID, device in entry.runtime_data.coordinator.data.items():
            async_add_entities(
                 BSKZephyrSensor(groupID, entry.runtime_data.coordinator, description)
                 for description in SENSOR_TYPES
            )
        

class BSKZephyrSensor(SensorEntity, CoordinatorEntity[DeviceDataUpdateCoordinator]):
    def __init__(self, groupID: str, coordinator: DeviceDataUpdateCoordinator, description: SensorEntityDescription):
         super().__init__(coordinator)
         
         self._attr_unique_id = f"{groupID}-{description.key}"
         self._attr_name = f"{coordinator.data[groupID].groupTitle} {description.name}"
         self._attr_device_info = DeviceInfo(
              connections={(CONNECTION_NETWORK_MAC, groupID)},
              name=coordinator.data[groupID].groupTitle,
              model=coordinator.data[groupID].deviceModel,
              sw_version=coordinator.data[groupID].device.version
         )
         self.coordinator = coordinator
         self.groupID = groupID
         self.entity_description = description

    async def async_added_to_hass(self) -> None:
         self.async_on_remove(self.coordinator.async_add_listener(self._handle_coordinator_update))
         self._handle_coordinator_update()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.native_value = getattr(self.coordinator.data[self.groupID].device, self.entity_description.key)
        self.async_write_ha_state()

    @property
    def state(self):
         return self.native_value
