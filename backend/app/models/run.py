from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, UTC
from enum import Enum


class RunStatus(str, Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class RunBase(BaseModel):
    agent_id: str = Field(..., description="Agent identifier")
    status: RunStatus = Field(default=RunStatus.STARTED, description="Run status")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    logs: Optional[List[str]] = Field(default_factory=list, description="Execution logs")
    command: Optional[str] = Field(
        default=None, description="Command to execute when running the agent"
    )


class RunCreate(RunBase):
    pass


class Run(RunBase):
    id: str = Field(..., description="Unique run identifier")
    model_config = ConfigDict(from_attributes=True)


class RunUpdate(BaseModel):
    status: Optional[RunStatus] = None
    logs: Optional[List[str]] = None


class RunListResponse(BaseModel):
    items: list[Run]
    total: int
    page: int
    page_size: int
    total_pages: int
