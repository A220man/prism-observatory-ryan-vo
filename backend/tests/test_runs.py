import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


async def _create_agent(client, name):
    resp = await client.post("/api/agents", json={"name": name})
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_run_executes_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        agent_id = await _create_agent(client, "Run Exec Agent")
        response = await client.post(
            "/api/runs", json={"agent_id": agent_id, "command": "echo hi"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["agent_id"] == agent_id
        # Triggering a run executes it to a terminal state with logs.
        assert data["status"] == "completed"
        assert data["command"] == "echo hi"
        assert isinstance(data["logs"], list) and len(data["logs"]) >= 1
        assert "id" in data and "created_at" in data


@pytest.mark.asyncio
async def test_create_run_unknown_agent_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/runs", json={"agent_id": "does-not-exist"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_run():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        agent_id = await _create_agent(client, "Get Run Agent")
        create_resp = await client.post("/api/runs", json={"agent_id": agent_id})
        assert create_resp.status_code == 201
        run_id = create_resp.json()["id"]
        get_resp = await client.get(f"/api/runs/{run_id}")
        assert get_resp.status_code == 200
        run_data = get_resp.json()
        assert run_data["id"] == run_id
        assert run_data["status"] == "completed"


@pytest.mark.asyncio
async def test_list_runs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        agent_id = await _create_agent(client, "List Run Agent")
        await client.post("/api/runs", json={"agent_id": agent_id})
        await client.post("/api/runs", json={"agent_id": agent_id})
        response = await client.get("/api/runs")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        assert len(data["items"]) >= 2
