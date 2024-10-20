from fastapi import FastAPI

from .routes import router as api_router
from database.session import async_session_local
from database.base import Base

# Initialize the FastAPI application
app = FastAPI(title="FastAPI Main Service")

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    async with async_session_local.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Main Service"}