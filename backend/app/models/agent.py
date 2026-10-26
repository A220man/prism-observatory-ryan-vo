from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, UTC
from enum import Enum


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Agent name")
    description: Optional[str] = Field(None, max_length=500, description="Agent description")
    config: dict = Field(default_factory=dict, description="Agent configuration")


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    config: Optional[dict] = None
    status: Optional[AgentStatus] = None


class Agent(AgentBase):
    id: str = Field(..., description="Unique agent identifier")
    status: AgentStatus = Field(default=AgentStatus.ACTIVE, description="Agent status")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class AgentListResponse(BaseModel):
    items: list[Agent]
    total: int
    page: int
    page_size: int
    total_pages: int
