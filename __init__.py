from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import MyDeviceDataUpdateCoordinator
from .api import MyDeviceApiClient

# List the platforms that your integration will support
PLATFORMS = [Platform.SWITCH, Platform.COVER, Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up My Device from a config entry."""
    host = entry.data[CONF_HOST]

    # Create the API client and coordinator
    api_client = MyDeviceApiClient(host)
    coordinator = MyDeviceDataUpdateCoordinator(hass, api_client)

    # Fetch initial data so we have it when entities are set up
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator object for entities to access
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward the setup to the entity platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok