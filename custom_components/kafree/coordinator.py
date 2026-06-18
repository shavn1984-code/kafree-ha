"""Coordinator for Kafree."""
import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .api import KafreeApiClient
from .const import CONF_BASE_URL, CONF_SCAN_INTERVAL, CONF_SN, CONF_TOKEN, DEFAULT_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN
_LOGGER = logging.getLogger(__name__)

class KafreeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        token = entry.options.get(CONF_TOKEN) or entry.data.get(CONF_TOKEN, "")
        base_url = entry.options.get(CONF_BASE_URL) or entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
        self._sn = entry.options.get(CONF_SN) or entry.data.get(CONF_SN, "")
        self.client = KafreeApiClient(base_url=base_url, token=token)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))

    async def _async_update_data(self):
        data = {"ds": {}, "di": {}, "dd": {}, "ms": [], "dt": []}

        r = await self.client.get_device_data_by_user()
        if isinstance(r, dict) and isinstance(r.get("data"), list) and r["data"]:
            data["dt"] = r["data"]
            if not self._sn:
                self._sn = r["data"][0].get("deviceId", "")

        if not self._sn:
            _LOGGER.error("无法获取设备 SN")
            return data

        r = await self.client.get_drink_statistic(self._sn)
        if isinstance(r, dict) and isinstance(r.get("data"), dict):
            data["ds"] = r["data"]

        r = await self.client.get_device_status(self._sn)
        if isinstance(r, dict) and isinstance(r.get("data"), dict) and isinstance(r["data"].get("status"), dict):
            data["di"] = r["data"]["status"]

        r = await self.client.get_device_detail(self._sn)
        if isinstance(r, dict) and isinstance(r.get("data"), dict):
            data["dd"] = r["data"]

        r = await self.client.get_messages()
        if isinstance(r, dict) and isinstance(r.get("data"), dict):
            data["ms"] = r["data"].get("list", [])

        return data
