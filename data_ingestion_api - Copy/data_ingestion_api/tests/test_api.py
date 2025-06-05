import asyncio
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_priority_order():
    async with AsyncClient(app=app, base_url="http://test") as client:
        medium = await client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "MEDIUM"})
        await asyncio.sleep(1)
        high = await client.post("/ingest", json={"ids": [6, 7, 8, 9], "priority": "HIGH"})

        await asyncio.sleep(16)

        res = await client.get(f"/status/{medium.json()['ingestion_id']}")
        assert res.json()["status"] == "completed"

        res2 = await client.get(f"/status/{high.json()['ingestion_id']}")
        assert res2.json()["status"] == "completed"
