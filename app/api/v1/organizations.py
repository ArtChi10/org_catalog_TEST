from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, verify_api_key
from app.schemas.organization import OrganizationOut
from app.services.organization_service import (
    get_organization_by_id,
    get_organizations_by_building,
    search_organizations_by_name,
    get_organizations_by_activity,
    get_organizations_in_radius,
    get_organizations_in_bbox,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationOut, dependencies=[Depends(verify_api_key)])
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    org = get_organization_by_id(db, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/", response_model=list[OrganizationOut], dependencies=[Depends(verify_api_key)])
def list_organizations(
    building_id: int | None = None,
    activity_id: int | None = None,
    include_children: bool = False,
    name: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    radius_km: float | None = None,
    min_lat: float | None = None,
    max_lat: float | None = None,
    min_lon: float | None = None,
    max_lon: float | None = None,
    db: Session = Depends(get_db),
):
    if building_id is not None:
        return get_organizations_by_building(db, building_id)

    if activity_id is not None:
        return get_organizations_by_activity(db, activity_id, include_children)

    if name is not None:
        return search_organizations_by_name(db, name)

    if lat is not None and lon is not None and radius_km is not None:
        return get_organizations_in_radius(db, lat, lon, radius_km)

    if None not in (min_lat, max_lat, min_lon, max_lon):
        return get_organizations_in_bbox(db, min_lat, max_lat, min_lon, max_lon)

    return []