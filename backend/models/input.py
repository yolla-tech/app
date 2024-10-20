from pydantic import BaseModel

class BaseInput(BaseModel):
    location_a: str
    location_b: str
    servis_type: str = "default"
    extra_services: list[str] = []

class LetterInput(BaseInput):
    ...
    

class BoxProperties(BaseModel):
    width: float = 0
    height: float = 0
    length: float = 0
    weight: float = 0
    

class BoxInput(BaseInput):
    properties: BoxProperties