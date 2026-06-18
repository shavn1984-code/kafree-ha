"""API client for Kafree."""
import logging, httpx, json as j, time, base64
from .const import DEFAULT_BASE_URL
_LOGGER = logging.getLogger(__name__)

class KafreeApiError(Exception):
    pass

def _decode_user_id_from_token(token):
    try:
        parts = token.split(".")
        if len(parts) == 3:
            padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = j.loads(base64.urlsafe_b64decode(padded))
            return str(payload.get("id", ""))
    except Exception:
        pass
    return ""

class KafreeApiClient:
    def __init__(self, base_url=DEFAULT_BASE_URL, token=None, user_id=""):
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._user_id = user_id or _decode_user_id_from_token(token or "")
        self._client = httpx.AsyncClient(timeout=15.0, verify=False)

    def _h(self, extra=None):
        h = {"Authorization": f"Bearer {self._token}"} if self._token else {}
        if extra:
            h.update(extra)
        return h

    async def close(self):
        await self._client.aclose()

    async def _get(self, path, headers=None, params=None):
        try:
            r = await self._client.get(
                f"{self._base_url}{path}",
                headers=headers or self._h(),
                params=params,
            )
            return r.json() if r.status_code == 200 else {}
        except:
            return {}

    async def _post(self, path, headers=None, **kw):
        try:
            r = await self._client.post(
                f"{self._base_url}{path}", headers=headers or self._h(), **kw
            )
            return r.json() if r.status_code == 200 else {}
        except:
            return {}

    async def _mqtt_cmd(self, sn, payload):
        import aiomqtt

        ts = int(time.time() * 1000)
        info = await self._get(
            f"/api/iot-home-user/mini/app/getConnectInfo?userId={self._user_id}&timestamp={ts}"
        )
        if not info or not info.get("data"):
            _LOGGER.error("MQTT凭证获取失败")
            return False
        d = info["data"]
        try:
            async with aiomqtt.Client(
                hostname=self._base_url.replace("https://", ""),
                port=443,
                identifier=d["mqttClientId"],
                username=d["mqttUsername"],
                password=d["mqttPassword"],
                transport="websockets",
                websocket_path="/mqtt",
                tls_params=aiomqtt.TLSParameters(),
            ) as client:
                await client.publish(
                    f"device/{sn}/command", j.dumps(payload), qos=1
                )
                _LOGGER.info("MQTT指令已发送: %s", payload)
                return True
        except Exception as e:
            _LOGGER.error("MQTT发送失败: %s", e)
            return False

    async def get_drink_statistic(self, sn):
        return await self._get(
            f"/api/iot-home-user/iot-search-engine/drink-record/home/statistic/{sn}",
            headers=self._h({"Content-Type": "application/json"}),
        )

    async def get_device_status(self, sn):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" + \
             " AppleWebKit/537.36 MicroMessenger/7.0.20"
        return await self._post(
            "/api/iot-home-user/device-manager/organization/searchHomeDeviceStatus",
            headers=self._h({
                "Content-Type": "application/x-www-form-urlencoded",
                "x-request-from": "wechat-mini-program",
                "User-Agent": ua,
            }),
            data={"deviceId": sn},
        )

    async def get_device_detail(self, sn):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" + \
             " AppleWebKit/537.36 MicroMessenger/7.0.20"
        return await self._get(
            f"/api/iot-home-user/device-manager/organization/device/status/{sn}",
            headers=self._h({
                "x-request-from": "wechat-mini-program",
                "User-Agent": ua,
                "Accept": "*/*",
            }),
        )

    async def get_device_data_by_user(self):
        return await self._post(
            "/api/iot-home-user/getDeviceData/iotTemplate/byUserId",
            headers=self._h({
                "Content-Type": "application/x-www-form-urlencoded",
                "x-request-from": "wechat-mini-program",
                "Accept": "*/*",
            }),
            data={"userId": self._user_id},
        )

    async def get_messages(self):
        return await self._post(
            "/api/kafree-mall-portal/mallUserMessage/messageCenter/page",
            headers=self._h({"Content-Type": "application/json"}),
            json={"messageTypeList": [2], "messageId": None, "page": {"size": 5}},
        )

    async def get_remote_shutdown_list(self, sn):
        ts = int(time.time() * 1000)
        msg_id = f"kws8Kkbatw{ts}"
        return await self._get(
            "/api/iot-home-user/device-manager/web/remoteShutdownList",
            headers=self._h({
                "x-request-from": "wechat-mini-program",
                "Content-Type": "application/json",
            }),
            params={"deviceId": sn, "msgId": msg_id},
        )

    async def get_remote_boot_list(self, sn):
        ts = int(time.time() * 1000)
        msg_id = f"ccZaTQHhnn{ts}"
        return await self._get(
            "/api/iot-home-user/device-manager/web/remoteBootList",
            headers=self._h({
                "x-request-from": "wechat-mini-program",
                "Content-Type": "application/json",
            }),
            params={"deviceId": sn, "msgId": msg_id},
        )

    async def set_power(self, sn, on):
        return await self._mqtt_cmd(sn, {"power": 1 if on else 0})

    async def set_baby_lock(self, sn, locked):
        ts = int(time.time() * 1000)
        msg_id = f"WFWE4KnsHn{ts}"
        return await self._post(
            "/api/iot-home-user/device-manager/web/remoteBabyLock",
            headers=self._h({
                "x-request-from": "wechat-mini-program",
                "Content-Type": "application/x-www-form-urlencoded",
            }),
            data={"deviceId": sn, "lockedStatus": "1" if locked else "0", "msgId": msg_id},
        )
