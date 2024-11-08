from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator, model_validator

from typing_extensions import Annotated
from typing_extensions import Self

def check_between_value_validity(v: float) -> float:
    assert 0.0 <= v <= 1.0, f'Search weight {v} is not in the range of 0 and 1'
    return v

Weight = Annotated[float, AfterValidator(check_between_value_validity)]

class SearchWeights(BaseModel):
    price_weight: Weight = 0.6
    time_weight: Weight = 0.1
    
    walk_to_distance_weight: Weight = 0.05
    public_to_transport_distance_weight: Weight = 0.05
    car_to_distance_weight: Weight = 0.05
    
    walk_from_distance_weight: Weight = 0.05
    public_from_transport_distance_weight: Weight = 0.05
    car_from_distance_weight: Weight = 0.05
    
    @model_validator(mode='before')
    def check_weights(self) -> Self:
        total = self['price_weight'] + \
            self['time_weight'] + self['walk_to_distance_weight'] + \
            self['public_to_transport_distance_weight'] + self['car_to_distance_weight'] + \
            self['walk_from_distance_weight'] + self['public_from_transport_distance_weight'] + \
            self['car_from_distance_weight']
    
        assert total == 1.0, f'Sum of the search weights must be 1, total: {total}'
        
        return self
    
    