from pydantic import BaseModel


class Payload(BaseModel):
    city_a: str
    city_b: str
    weight: float = None
    width: float = None
    height: float = None
    length: float = None
    type: str = "letter" 
    from_address: bool = False
    to_address: bool = False