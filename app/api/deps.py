from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )