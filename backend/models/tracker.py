from pydantic import BaseModel, ConfigDict

from datetime import datetime


class TrackedPackageMovement(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    id: int
    is_active: bool
    description: str
    detail_description: str
    title: str
    date: datetime
    branch: str | None
    province: str | None
    district: str | None
    external_location: str | None
    status: str
    status_slug: str | None


class TrackedPackage(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    company_id: int
    is_active: bool = False
    company_name: str
    is_delivered: bool = False
    status_description: str | None
    receiver: str | None
    sender: str | None
    send_date: datetime | None
    delivered_date: datetime | None
    additional_data: str | None
    branch_departure: str | None
    branch_delivery: str | None
    movement: list[TrackedPackageMovement]
