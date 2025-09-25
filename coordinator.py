from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MyDeviceApiClient

_LOGGER = logging.getLogger(__name__)

class MyDeviceDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, api_client: MyDeviceApiClient):
        """Initialize."""
        self.api = api_client
        # Poll every 5 seconds as noted in your API list
        super().__init__(
            hass,
            _LOGGER,
            name="My Device Status",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to make it easier
        for your entities to use.
        """
        try:
            # This is the single polling call for all entities
            return await self.api.async_get_status()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")