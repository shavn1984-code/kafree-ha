#!/usr/bin/env python3
"""验证咖啡自由 API 脚本"""
import httpx, json, asyncio

TOKEN = "你的Token"
BASE = "https://kafree-app-cn.coffee-iot.com"
SN = "SF1BWCC250500170082"

headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

async def test():
    endpoints = [
        ("饮品统计", "GET", f"/api/iot-home-user/iot-search-engine/drink-record/home/statistic/{SN}"),
        ("设备状态", "GET", "/api/iot-home-user/device-manager/organization/searchHomeDeviceStatus"),
    ]
    async with httpx.AsyncClient(timeout=10.0) as c:
        for name, method, ep in endpoints:
            url = f"{BASE}{ep}"
            try:
                r = await c.request(method, url, headers=headers)
                print(f"\n{'='*50}\n{name}: HTTP {r.status_code}\nURL: {url}")
                if r.status_code == 200:
                    print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:600])
                else:
                    print(f"错误: {r.text[:300]}")
            except Exception as e:
                print(f"\n❌ {name}: {e}")

asyncio.run(test())
