from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db, verify_api_key
from app.models.building import Building
from app.schemas.building import BuildingOut

router = APIRouter(prefix="/buildings", tags=["Buildings"])


@router.get("/", response_model=list[BuildingOut], dependencies=[Depends(verify_api_key)])
def list_buildings(db: Session = Depends(get_db)):
    return db.execute(select(Building)).scalars().all()