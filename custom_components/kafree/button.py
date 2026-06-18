"""Button platform for Kafree coffee machine power control."""
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        KafreeButton(coordinator, entry, "开机", "power_on"),
        KafreeButton(coordinator, entry, "关机", "power_off"),
        KafreeButton(coordinator, entry, "解锁", "lock_off"),
        KafreeButton(coordinator, entry, "锁定", "lock_on"),
    ])

class KafreeButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry, action_name, action_key):
        super().__init__(coordinator)
        self._action_key = action_key
        self._attr_unique_id = f"{entry.entry_id}_button_{action_key}"
        self._attr_name = "咖啡自由 " + action_name
        self._attr_icon = "mdi:lock" if "lock" in action_key else "mdi:power"

    async def async_press(self):
        actions = {
            "power_on": self._do_power_on,
            "power_off": self._do_power_off,
            "lock_on": self._do_lock_on,
            "lock_off": self._do_lock_off,
        }
        action = actions.get(self._action_key)
        if action:
            await action()
        # 强制刷新所有传感器数据
        await self.coordinator.async_request_refresh()

    async def _do_power_on(self):
        _LOGGER.info("查询远程开机状态...")
        result = await self.coordinator.client.get_remote_boot_list(
            self.coordinator._sn
        )
        if isinstance(result, dict):
            _LOGGER.info("远程开机列表返回: %s", result.get("message", "未知"))
        _LOGGER.info("咖啡机开机指令发送中...")
        ok = await self.coordinator.client.set_power(
            self.coordinator._sn, on=True
        )
        if ok:
            _LOGGER.info("咖啡机开机指令已发送")
        else:
            _LOGGER.error("咖啡机开机指令发送失败")

    async def _do_power_off(self):
        _LOGGER.info("查询远程关机状态...")
        result = await self.coordinator.client.get_remote_shutdown_list(
            self.coordinator._sn
        )
        if isinstance(result, dict):
            _LOGGER.info("远程关机列表返回: %s", result.get("message", "未知"))
        _LOGGER.info("咖啡机关机指令发送中...")
        ok = await self.coordinator.client.set_power(
            self.coordinator._sn, on=False
        )
        if ok:
            _LOGGER.info("咖啡机关机指令已发送")
        else:
            _LOGGER.error("咖啡机关机指令发送失败")

    async def _do_lock_on(self):
        _LOGGER.info("关锁指令发送中...")
        result = await self.coordinator.client.set_baby_lock(
            self.coordinator._sn, locked=True
        )
        if isinstance(result, dict) and result.get("success"):
            _LOGGER.info("关锁指令已发送")
        else:
            _LOGGER.error("关锁指令发送失败")

    async def _do_lock_off(self):
        _LOGGER.info("开锁指令发送中...")
        result = await self.coordinator.client.set_baby_lock(
            self.coordinator._sn, locked=False
        )
        if isinstance(result, dict) and result.get("success"):
            _LOGGER.info("开锁指令已发送")
        else:
            _LOGGER.error("开锁指令发送失败")
