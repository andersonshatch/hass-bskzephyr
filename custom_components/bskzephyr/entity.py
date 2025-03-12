from .sensor import DeviceDataUpdateCoordinator
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class BSKZephyrEntity(CoordinatorEntity[DeviceDataUpdateCoordinator]):
    """Base implementation of BSK Zephyr entities."""

    def __init__(
        self,
        coordinator: DeviceDataUpdateCoordinator,
        entity_description: EntityDescription,
        property_id: str,
    ):
        super().__init__(coordinator)

        self.entity_description = entity_description
        self.property_id = property_id

        self._attr_device_info = dr.DeviceInfo(identifiers={(DOMAIN,)})
