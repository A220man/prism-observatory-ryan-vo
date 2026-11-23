from typing import Optional
from datetime import datetime, UTC
import uuid

from app.models.run import Run, RunCreate, RunUpdate, RunStatus, RunListResponse


class RunService:
    def __init__(self):
        self._runs: dict[str, Run] = {}

    def create(self, run_data: RunCreate) -> Run:
        run_id = str(uuid.uuid4())
        now = datetime.now(UTC)
        run = Run(
            id=run_id,
            agent_id=run_data.agent_id,
            status=RunStatus.STARTED,
            created_at=now,
            logs=[],
            command=run_data.command,
        )
        self._runs[run_id] = run
        return run

    def get(self, run_id: str) -> Optional[Run]:
        return self._runs.get(run_id)

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        agent_id: Optional[str] = None,
        status: Optional[RunStatus] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> RunListResponse:
        runs = list(self._runs.values())
        if agent_id:
            runs = [r for r in runs if r.agent_id == agent_id]
        if status:
            runs = [r for r in runs if r.status == status]
        # Validate sort_by
        valid_sort_fields = {"agent_id", "created_at", "status"}
        if sort_by not in valid_sort_fields:
            sort_by = "created_at"
        reverse = sort_order.lower() == "desc"
        runs.sort(key=lambda r: getattr(r, sort_by), reverse=reverse)
        total = len(runs)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        page = max(1, min(page, total_pages))
        start = (page - 1) * page_size
        end = start + page_size
        items = runs[start:end]
        return RunListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def update(self, run_id: str, run_data: RunUpdate) -> Optional[Run]:
        run = self._runs.get(run_id)
        if not run:
            return None
        if run_data.status is not None:
            run.status = run_data.status
        if run_data.logs is not None:
            run.logs = run_data.logs
        return run

    def delete(self, run_id: str) -> bool:
        if run_id in self._runs:
            del self._runs[run_id]
            return True
        return False


run_service = RunService()
