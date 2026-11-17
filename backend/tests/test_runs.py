import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_run():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/runs", json={"agent_id": "test-agent"})
        assert response.status_code == 201
        data = response.json()
        assert data["agent_id"] == "test-agent"
        assert data["status"] == "started"
        assert "id" in data
        assert "created_at" in data
        return data["id"]

@pytest.mark.asyncio
async def test_get_run():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/runs", json={"agent_id": "agent2"})
        assert create_resp.status_code == 201
        run_id = create_resp.json()["id"]
        get_resp = await client.get(f"/api/runs/{run_id}")
        assert get_resp.status_code == 200
        run_data = get_resp.json()
        assert run_data["id"] == run_id

@pytest.mark.asyncio
async def test_list_runs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a few runs
        await client.post("/api/runs", json={"agent_id": "list-run-a"})
        await client.post("/api/runs", json={"agent_id": "list-run-b"})
        response = await client.get("/api/runs")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        assert len(data["items"]) >= 2
