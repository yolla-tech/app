from pydantic import BaseModel


class Payload(BaseModel):
    city_a: str
    city_b: str
    weight: float | None = None
    width: float | None = None
    height: float | None = None
    length: float | None = None
    type: str = "letter" 
    from_address: bool = False
    to_address: bool = False