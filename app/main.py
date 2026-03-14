from fastapi import FastAPI
from app.api.v1.activities import router as activities_router
from app.api.v1.buildings import router as buildings_router
from app.api.v1.organizations import router as organizations_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(organizations_router, prefix=settings.API_V1_PREFIX)
app.include_router(buildings_router, prefix=settings.API_V1_PREFIX)
app.include_router(activities_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Organizations Catalog API"}