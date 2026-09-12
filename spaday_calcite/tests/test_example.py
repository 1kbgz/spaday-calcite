import asyncio

import httpx

from spaday_calcite import example


def test_example_serves_calcite_workspace():
    async def request():
        transport = httpx.ASGITransport(app=example.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/tree.json")

    response = asyncio.run(request())
    assert response.status_code == 200
    for tag in ("calcite-navigation", "calcite-card", "calcite-list", "calcite-table"):
        assert tag in response.text
