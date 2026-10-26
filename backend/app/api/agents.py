from fastapi import APIRouter, HTTPException, Query, status
from app.models.agent import Agent, AgentCreate, AgentUpdate, AgentStatus, AgentListResponse
from app.services.agent_service import agent_service

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def create_agent(agent_data: AgentCreate):
    return agent_service.create(agent_data)


@router.get("", response_model=AgentListResponse)
async def list_agents(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: AgentStatus | None = Query(None, description="Filter by status"),
    name: str | None = Query(None, description="Filter by name (partial match)"),
):
    return agent_service.list(page=page, page_size=page_size, status=status, name_filter=name)


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    agent = agent_service.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.patch("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, agent_data: AgentUpdate):
    agent = agent_service.update(agent_id, agent_data)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str):
    deleted = agent_service.delete(agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
