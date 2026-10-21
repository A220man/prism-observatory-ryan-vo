# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

project-skeleton

## Roadmap

### project-skeleton — FastAPI + React Project Skeleton with Health Check

Status: done

Acceptance:
- Backend FastAPI app starts and responds to /healthz
- Frontend Vite React app builds and serves
- Docker Compose brings up both services
- Basic pytest and vitest test suites pass

Implementation: `backend/app/main.py`, `backend/app/api/health.py`, `backend/requirements.txt`, `backend/Dockerfile`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/index.css`, `frontend/index.html`, `frontend/Dockerfile`, `frontend/nginx.conf`, `docker-compose.yaml`

Tests: `backend/tests/test_health.py`, `frontend/tests/App.test.tsx`

### agent-management — Agent CRUD and Listing

Status: planned

Acceptance:
- Create, read, update, delete agents via API
- List agents with pagination and filtering
- Frontend dashboard shows agent list with actions

### agent-runs — Agent Run History and Execution

Status: planned

Acceptance:
- Trigger agent runs via API
- View run history with status and logs
- Frontend shows run details and streaming logs

### observability — Metrics and Observability Dashboard

Status: planned

Acceptance:
- Collect and display agent performance metrics
- Token usage, latency, success rate charts
- Export metrics as CSV/JSON

