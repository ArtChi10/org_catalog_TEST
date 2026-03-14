from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db, verify_api_key
from app.models.activity import Activity
from app.schemas.activity import ActivityOut

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/", response_model=list[ActivityOut], dependencies=[Depends(verify_api_key)])
def list_activities(db: Session = Depends(get_db)):
    return db.execute(select(Activity)).scalars().all()