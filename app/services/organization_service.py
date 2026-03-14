from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity
from app.utils.geo import haversine
from app.services.activity_service import collect_descendant_ids


def get_organization_by_id(db: Session, organization_id: int):
    stmt = (
        select(Organization)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(Organization.id == organization_id)
    )
    return db.execute(stmt).scalars().first()


def get_organizations_by_building(db: Session, building_id: int):
    stmt = (
        select(Organization)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(Organization.building_id == building_id)
    )
    return db.execute(stmt).unique().scalars().all()


def search_organizations_by_name(db: Session, query: str):
    stmt = (
        select(Organization)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(Organization.name.ilike(f"%{query}%"))
    )
    return db.execute(stmt).unique().scalars().all()


def get_organizations_by_activity(db: Session, activity_id: int, include_children: bool = False):
    activity = db.get(Activity, activity_id)
    if not activity:
        return []

    activity_ids = [activity_id]
    if include_children:
        activity_ids = collect_descendant_ids(activity)

    stmt = (
        select(Organization)
        .join(Organization.activities)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(Activity.id.in_(activity_ids))
    )
    return db.execute(stmt).unique().scalars().all()


def get_buildings_in_radius(db: Session, lat: float, lon: float, radius_km: float):
    buildings = db.execute(select(Building)).scalars().all()
    matched = []

    for building in buildings:
        distance = haversine(lat, lon, building.latitude, building.longitude)
        if distance <= radius_km:
            matched.append(building.id)

    return matched


def get_organizations_in_radius(db: Session, lat: float, lon: float, radius_km: float):
    building_ids = get_buildings_in_radius(db, lat, lon, radius_km)
    if not building_ids:
        return []

    stmt = (
        select(Organization)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(Organization.building_id.in_(building_ids))
    )
    return db.execute(stmt).unique().scalars().all()


def get_organizations_in_bbox(
    db: Session,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
):
    stmt = (
        select(Organization)
        .join(Organization.building)
        .options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )
        .where(
            Building.latitude >= min_lat,
            Building.latitude <= max_lat,
            Building.longitude >= min_lon,
            Building.longitude <= max_lon,
        )
    )
    return db.execute(stmt).unique().scalars().all()