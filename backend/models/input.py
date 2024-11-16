from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

from typing_extensions import Annotated

def check_location_validity(s: str) -> str:
    assert len(s) != 0
    return s.lower()

def check_property_validaty(v: float) -> float:
    assert v > 0
    return v

Location = Annotated[str, AfterValidator(check_location_validity)]

Property = Annotated[float, AfterValidator(check_property_validaty)]

class BaseInput(BaseModel):
    location_a: Location
    location_b: Location
    servis_type: str = "default"
    extra_services: list[str] = []

class LetterInput(BaseInput):
    ...
    

class BoxProperties(BaseModel):
    width: Property = 1
    height: Property = 1
    length: Property = 1
    weight: Property = 1
    

class BoxInput(BaseInput):
    properties: BoxProperties