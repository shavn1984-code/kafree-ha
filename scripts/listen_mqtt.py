#!/usr/bin/env python3
"""咖啡自由 MQTT 监听工具。
用法: python3 listen_mqtt.py
"""
import httpx, json, asyncio, time, sys

TOKEN = "你的Token"
BASE = "https://kafree-app-cn.coffee-iot.com"
USER_ID = "52624"
SN = "SF1BWCC250500170082"

async def main():
    async with httpx.AsyncClient(timeout=10.0, verify=False) as http:
        ts = int(time.time() * 1000)
        r = await http.get(f"{BASE}/api/iot-home-user/mini/app/getConnectInfo?userId={USER_ID}&timestamp={ts}",
            headers={"Authorization": f"Bearer {TOKEN}", "x-request-from": "wechat-mini-program"})
        info = r.json()["data"]

    import aiomqtt
    async with aiomqtt.Client(
        hostname="kafree-app-cn.coffee-iot.com",
        port=443,
        identifier=info["mqttClientId"],
        username=info["mqttUsername"],
        password=info["mqttPassword"],
        transport="websockets",
        websocket_path="/mqtt",
        tls_params=aiomqtt.TLSParameters(),
    ) as client:
        await client.subscribe(f"device/{SN}/#")
        print(f"✅ 已连接，监听 device/{SN}/# ...")
        async for msg in client.messages:
            print(f"\n📩 {msg.topic}")
            print(f"   {msg.payload.decode()[:300]}")

asyncio.run(main())
