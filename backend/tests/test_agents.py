import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/agents",
            json={"name": "Test Agent", "description": "A test agent", "config": {"model": "gpt-4"}},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Agent"
        assert data["description"] == "A test agent"
        assert data["config"] == {"model": "gpt-4"}
        assert data["status"] == "active"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        return data["id"]


@pytest.mark.asyncio
async def test_get_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create first
        create_resp = await client.post("/api/agents", json={"name": "Get Test Agent"})
        assert create_resp.status_code == 201
        agent_id = create_resp.json()["id"]

        # Get it
        response = await client.get(f"/api/agents/{agent_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == agent_id
        assert data["name"] == "Get Test Agent"


@pytest.mark.asyncio
async def test_get_nonexistent_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/agents/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_agents():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create a few agents
        await client.post("/api/agents", json={"name": "Agent A"})
        await client.post("/api/agents", json={"name": "Agent B"})
        await client.post("/api/agents", json={"name": "Agent C"})

        response = await client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 3
        assert data["page"] == 1
        assert data["page_size"] == 20
        assert len(data["items"]) >= 3


@pytest.mark.asyncio
async def test_list_agents_pagination():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create agents
        for i in range(5):
            await client.post("/api/agents", json={"name": f"Page Agent {i}"})

        # Test page 1 with size 2
        response = await client.get("/api/agents?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert len(data["items"]) == 2
        assert data["total_pages"] >= 3

        # Test page 2
        response = await client.get("/api/agents?page=2&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_list_agents_filter_by_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create agent and update status
        create_resp = await client.post("/api/agents", json={"name": "Status Filter Agent"})
        agent_id = create_resp.json()["id"]
        await client.patch(f"/api/agents/{agent_id}", json={"status": "inactive"})

        # Filter by active
        response = await client.get("/api/agents?status=active")
        assert response.status_code == 200
        data = response.json()
        for agent in data["items"]:
            assert agent["status"] == "active"

        # Filter by inactive
        response = await client.get("/api/agents?status=inactive")
        assert response.status_code == 200
        data = response.json()
        for agent in data["items"]:
            assert agent["status"] == "inactive"


@pytest.mark.asyncio
async def test_list_agents_filter_by_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/agents", json={"name": "Special Agent Alpha"})
        await client.post("/api/agents", json={"name": "Regular Agent Beta"})

        response = await client.get("/api/agents?name=special")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        for agent in data["items"]:
            assert "special" in agent["name"].lower()


@pytest.mark.asyncio
async def test_update_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/agents", json={"name": "Original Name"})
        agent_id = create_resp.json()["id"]

        response = await client.patch(
            f"/api/agents/{agent_id}",
            json={"name": "Updated Name", "description": "Updated description"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_update_nonexistent_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.patch("/api/agents/nonexistent", json={"name": "New Name"})
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post("/api/agents", json={"name": "To Delete"})
        agent_id = create_resp.json()["id"]

        response = await client.delete(f"/api/agents/{agent_id}")
        assert response.status_code == 204

        # Verify deleted
        get_resp = await client.get(f"/api/agents/{agent_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete("/api/agents/nonexistent")
        assert response.status_code == 404
@pytest.mark.asyncio
async def test_create_duplicate_agent_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create first agent
        await client.post("/api/agents", json={"name": "Duplicate Test Agent"})
        # Try to create second agent with same name
        response = await client.post("/api/agents", json={"name": "Duplicate Test Agent"})
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_duplicate_agent_name_case_insensitive():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create first agent
        await client.post("/api/agents", json={"name": "Case Test Agent"})
        # Try to create second agent with same name different case
        response = await client.post("/api/agents", json={"name": "CASE TEST AGENT"})
        assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_agent_duplicate_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create two agents
        resp1 = await client.post("/api/agents", json={"name": "Agent One"})
        agent1_id = resp1.json()["id"]
        await client.post("/api/agents", json={"name": "Agent Two"})
        # Try to update agent one to have agent two's name
        response = await client.patch(f"/api/agents/{agent1_id}", json={"name": "Agent Two"})
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_agents_sort_by_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create agents with names that sort differently
        await client.post("/api/agents", json={"name": "Zeta Agent"})
        await client.post("/api/agents", json={"name": "Alpha Agent"})
        await client.post("/api/agents", json={"name": "Beta Agent"})
        # Sort by name ascending
        response = await client.get("/api/agents?sort_by=name&sort_order=asc&page_size=10")
        assert response.status_code == 200
        data = response.json()
        names = [agent["name"] for agent in data["items"]]
        # Should be sorted alphabetically
        assert names == sorted(names)


@pytest.mark.asyncio
async def test_list_agents_sort_by_created_at_desc():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/agents", json={"name": "First Agent"})
        await client.post("/api/agents", json={"name": "Second Agent"})
        # Sort by created_at descending (default)
        response = await client.get("/api/agents?sort_by=created_at&sort_order=desc&page_size=10")
        assert response.status_code == 200
        data = response.json()
        # Second agent should come first (newer)
        assert data["items"][0]["name"] == "Second Agent"
        assert data["items"][1]["name"] == "First Agent"


@pytest.mark.asyncio
async def test_list_agents_sort_by_updated_at():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/agents", json={"name": "Update Sort Agent"})
        agent_id = resp.json()["id"]
        # Update the agent to change updated_at
        await client.patch(f"/api/agents/{agent_id}", json={"description": "Updated"})
        # Sort by updated_at descending
        response = await client.get("/api/agents?sort_by=updated_at&sort_order=desc&page_size=10")
        assert response.status_code == 200
        data = response.json()
        # Updated agent should be first
        assert data["items"][0]["name"] == "Update Sort Agent"


@pytest.mark.asyncio
async def test_list_agents_invalid_sort_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/agents", json={"name": "Sort Test Agent"})
        # Invalid sort field should default to created_at
        response = await client.get("/api/agents?sort_by=invalid_field&sort_order=asc&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1
