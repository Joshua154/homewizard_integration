from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Assume the coordinator.data from /get-status looks like:
    # { "switches": [ {"id": "123", "name": "Living Room Lamp", "state": "on"}, ... ] }
    switches = [
        MyDeviceSwitch(coordinator, switch_data)
        for switch_data in coordinator.data.get("switches", [])
    ]
    async_add_entities(switches)


class MyDeviceSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a My Device Switch."""

    def __init__(self, coordinator, switch_data):
        super().__init__(coordinator)
        self._id = switch_data["id"]

        # Set static properties
        self._attr_name = switch_data["name"]
        self._attr_unique_id = f"switch_{self._id}"
        # You can add more device info attributes here

    @property
    def is_on(self):
        """Return true if the switch is on."""
        # Get the latest state from the coordinator's data
        # This requires you to parse the data structure from your device
        device_data = next((s for s in self.coordinator.data.get("switches", []) if s["id"] == self._id), None)
        if device_data:
            return device_data["state"] == "on"
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.coordinator.api.async_set_switch(self._id, "on")
        # After sending a command, ask the coordinator to refresh data
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.coordinator.api.async_set_switch(self._id, "off")
        await self.coordinator.async_request_refresh()