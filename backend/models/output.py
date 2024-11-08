from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid

class BillItem(BaseModel):
    name: str
    price: float


#distances are measured in time
class Route(BaseModel):
    walk_distance: timedelta = timedelta()
    public_transport_distance: timedelta = timedelta()
    car_distance: timedelta = timedelta()


class Bill(BaseModel):
    id: str = str(uuid.uuid4())
    service_name: str
    items: list[BillItem] = []
    total_price: float = 0.0
    expected_time: datetime | None
    to_route: Route
    from_route: Route
    from_address: bool = False
    to_address: bool = False
    link: str | None = None
    
    def __lt__(self, other: "Bill") -> bool:
        if not isinstance(other, Bill):
            return NotImplemented
        return self.id < other.id