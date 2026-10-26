from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.agents import router as agents_router

app = FastAPI(
    title="Prism Observatory",
    description="The open-source app everyone uses to manage agents at work",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api")
app.include_router(agents_router, prefix="/api")


@app.get("/")
async def root():
    return {"name": "Prism Observatory", "version": "0.1.0", "status": "running"}