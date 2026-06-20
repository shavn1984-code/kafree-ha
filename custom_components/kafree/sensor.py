"""Sensor platform for Kafree."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "device_status": {"name": "咖啡机状态", "icon": "mdi:coffee-maker"},
    "baby_lock": {"name": "童锁", "icon": "mdi:account-child"},
    "brewer_clean": {"name": "冲泡器清洗", "icon": "mdi:barrel", "unit": "%"},
    "descaling": {"name": "除垢清洗", "icon": "mdi:water-pump", "unit": "%"},
    "milk_clean": {"name": "奶沫器清洗", "icon": "mdi:cup", "unit": "%"},
    "clean_score": {"name": "当前清洁分", "icon": "mdi:broom", "unit": "分"},
    "total_cups": {"name": "已制作杯数", "icon": "mdi:coffee-to-go", "unit": "杯"},
    "bean_total": {"name": "累计咖啡豆", "icon": "mdi:coffee", "unit": "g"},
    "water_total": {"name": "累计水量", "icon": "mdi:water", "unit": "ml"},
    "milk_total": {"name": "累计牛奶", "icon": "mdi:cup", "unit": "ml"},
    "save_money": {"name": "比咖啡店节省", "icon": "mdi:cash", "unit": "元"},
    "black_coffee": {"name": "黑咖", "icon": "mdi:coffee", "unit": "杯"},
    "milk_coffee": {"name": "奶咖", "icon": "mdi:coffee", "unit": "杯"},
    "other_drink": {"name": "其他饮料", "icon": "mdi:cup", "unit": "杯"},
    "device_msg": {"name": "设备消息", "icon": "mdi:message-alert"},
    "bean_remain": {"name": "豆仓", "icon": "mdi:coffee"},
    "water_panel": {"name": "蓄水盘", "icon": "mdi:tray"},
    "water_temp": {"name": "水温", "icon": "mdi:thermometer"},
    "water_level": {"name": "水箱", "icon": "mdi:water"},
    "milk_foam": {"name": "奶泡器", "icon": "mdi:cup"},
    "device_template_status": {"name": "设备状态", "icon": "mdi:chip"},
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(KafreeSensor(coordinator, entry, k, v) for k, v in SENSORS.items())

class KafreeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, st, config):
        super().__init__(coordinator)
        self._st = st
        self._attr_unique_id = f"{entry.entry_id}_{st}"
        self._attr_name = "咖啡自由 " + config["name"]
        self._attr_icon = config.get("icon")
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_should_poll = False

    @callback
    def _handle_coordinator_update(self):
        if self.coordinator.data is None:
            self._attr_native_value = None
        else:
            try:
                self._attr_native_value = self._val(self.coordinator.data)
            except Exception as e:
                self._attr_native_value = None
        self.async_write_ha_state()

    def _val(self, d):
        tp = self._st
        dd = d.get("ds") if isinstance(d.get("ds"), dict) else {}
        dc = dd.get("cleanScore", {}) if isinstance(dd, dict) else {}
        di = d.get("di") if isinstance(d.get("di"), dict) else {}
        dv = d.get("dd") if isinstance(d.get("dd"), dict) else {}
        ml = d.get("ms") if isinstance(d.get("ms"), list) else []
        dt = d.get("dt") if isinstance(d.get("dt"), list) else []

        def p(v):
            return round(v * 100, 0) if v is not None else None

        m = {
            "device_status": (di.get("deviceStatus"), ["休眠","在线"], "离线"),
            "baby_lock": (di.get("babyLockStatus"), ["关闭","开启"], "未知"),
            "bean_remain": (dv.get("beanRemain"), ["正常","异常"], None),
            "water_panel": (dv.get("waterPanelFix"), ["正常","异常"], None),
            "water_level": (dv.get("waterBoxLevel"), ["正常","异常"], None),
            "milk_foam": (dv.get("milkFoamStatus"), ["正常","异常"], None),
            "water_temp": (dv.get("waterTemperature"), ["正常","异常"], "0"),
            "brewer_clean": (p(dc.get("busterCleaning")), None, None),
            "descaling": (p(dc.get("descaling")), None, None),
            "milk_clean": (p(dc.get("milkFrotherCleaning")), None, None),
            "clean_score": (dc.get("scoreTotal"), None, None),
            "total_cups": (dd.get("drinkTotalCount"), None, None),
            "bean_total": (dd.get("coffeeAmount"), None, None),
            "water_total": (dd.get("water"), None, None),
            "milk_total": (dd.get("milks"), None, None),
            "save_money": (dd.get("saveMoney"), None, None),
            "black_coffee": (dd.get("blackCoffeeCount"), None, None),
            "milk_coffee": (dd.get("milkCoffeeCount"), None, None),
            "other_drink": (dd.get("otherDrinkCount"), None, None),
            "device_msg": (
                str(ml[0].get("content") or ml[0].get("deviceMessageMsg") or "无消息")
                if ml else "无消息", None, None,
            ),
            "device_template_status": (
                dt[0].get("deviceStatus") if dt else None, None, None,
            ),
        }
        if tp == "device_template_status":
            v = dt[0].get("deviceStatus") if dt else None
            if v == "0":
                return "正常"
            elif v == "2":
                return "离线"
            elif v == "6":
                return "休眠"
            elif v in ("053", "05", "653"):
                return "缺料"
            elif v == "65":
                return "奶泡器缺失"
            elif v == "55":
                return "蓄水盘缺失"
            return v
        if tp in m:
            v, labels, fb = m[tp]
            if labels:
                return labels[0] if v == "0" else labels[1] if v == "1" else (fb if fb else v)
            return v
        return None
