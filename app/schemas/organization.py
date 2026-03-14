from pydantic import BaseModel, ConfigDict
from app.schemas.building import BuildingOut
from app.schemas.activity import ActivityOut


class PhoneOut(BaseModel):
    id: int
    number: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationOut(BaseModel):
    id: int
    name: str
    building: BuildingOut
    phones: list[PhoneOut]
    activities: list[ActivityOut]

    model_config = ConfigDict(from_attributes=True)