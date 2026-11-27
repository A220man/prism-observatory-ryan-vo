from fastapi import APIRouter, HTTPException, Query, status
from app.models.run import Run, RunCreate, RunUpdate, RunStatus, RunListResponse
from app.services.run_service import run_service

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", response_model=Run, status_code=status.HTTP_201_CREATED)
async def create_run(run_data: RunCreate):
    try:
        return run_service.create(run_data)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=RunListResponse)
async def list_runs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    agent_id: str | None = Query(None),
    status: RunStatus | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
):
    return run_service.list(
        page=page,
        page_size=page_size,
        agent_id=agent_id,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/{run_id}", response_model=Run)
async def get_run(run_id: str):
    run = run_service.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.patch("/{run_id}", response_model=Run)
async def update_run(run_id: str, run_data: RunUpdate):
    run = run_service.update(run_id, run_data)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_run(run_id: str):
    deleted = run_service.delete(run_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Run not found")
