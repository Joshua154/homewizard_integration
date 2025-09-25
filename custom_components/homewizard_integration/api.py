import aiohttp


class MyDeviceApiClient:
    """API Client for My Device."""

    def __init__(self, host: str):
        self._host = host
        # The base URL from your suntimes example looks complex. Let's assume it's constructed.
        # This is a guess, you may need to adjust!
        self._base_url = f"http://{host}/98omsa2u1h"
        self._session = aiohttp.ClientSession()

    async def async_handshake(self) -> bool:
        """Perform handshake to check connectivity."""
        # The handshake uses a different URL structure
        url = f"http://{self._host}/handshake/android/3/1"
        async with self._session.get(url) as response:
            response.raise_for_status()
            return True

    async def async_get_status(self) -> dict:
        """Get status of all devices."""
        url = f"{self._base_url}/get-status"
        async with self._session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def async_set_switch(self, switch_id: str, state: str) -> bool:
        """Set the state of a switch (on/off)."""
        url = f"{self._base_url}/sw/{switch_id}/{state}"
        async with self._session.get(url) as response:
            response.raise_for_status()
            return True

    async def async_control_somfy(self, device_id: str, direction: str) -> bool:
        """Control a Somfy cover (up/down/stop)."""
        url = f"{self._base_url}/sf/{device_id}/{direction}"
        async with self._session.get(url) as response:
            response.raise_for_status()
            return True

    # ... add other methods for presets, radiators, etc.