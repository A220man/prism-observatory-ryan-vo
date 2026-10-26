from typing import Optional
from datetime import datetime, UTC
import uuid

from app.models.agent import Agent, AgentCreate, AgentUpdate, AgentStatus, AgentListResponse


class AgentService:
    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def create(self, agent_data: AgentCreate) -> Agent:
        agent_id = str(uuid.uuid4())
        now = datetime.now(UTC)
        agent = Agent(
            id=agent_id,
            name=agent_data.name,
            description=agent_data.description,
            config=agent_data.config,
            status=AgentStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        self._agents[agent_id] = agent
        return agent

    def get(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[AgentStatus] = None,
        name_filter: Optional[str] = None,
    ) -> AgentListResponse:
        agents = list(self._agents.values())

        if status:
            agents = [a for a in agents if a.status == status]

        if name_filter:
            name_lower = name_filter.lower()
            agents = [a for a in agents if name_lower in a.name.lower()]

        agents.sort(key=lambda a: a.created_at, reverse=True)

        total = len(agents)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        page = max(1, min(page, total_pages))

        start = (page - 1) * page_size
        end = start + page_size
        items = agents[start:end]

        return AgentListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def update(self, agent_id: str, agent_data: AgentUpdate) -> Optional[Agent]:
        agent = self._agents.get(agent_id)
        if not agent:
            return None

        update_data = agent_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)

        agent.updated_at = datetime.now(UTC)
        return agent

    def delete(self, agent_id: str) -> bool:
        if agent_id in self._agents:
            del self._agents[agent_id]
            return True
        return False


agent_service = AgentService()
