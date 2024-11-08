from models.output import Bill
from models.input import LetterInput, BoxInput
from models.search_weights import SearchWeights
from services.cargo_services.base import BaseService
    

class CargoSearchManager:
    def __init__(self, services: list[BaseService] = []) -> None:
        self.services = services
    
    def score_bill(self, bill: Bill, weights: SearchWeights) -> float:
        price_score = bill.total_price * weights.price_weight
        time_score = bill.expected_time.timestamp() * weights.time_weight if bill.expected_time is not None else 0
        
        walk_to_score = bill.to_route.walk_distance.total_seconds() * weights.walk_to_distance_weight
        car_to_score = bill.to_route.car_distance.total_seconds() * weights.car_to_distance_weight
        public_to_score = bill.to_route.public_transport_distance.total_seconds() * weights.public_to_transport_distance_weight
        
        walk_from_score = bill.from_route.walk_distance.total_seconds() * weights.walk_from_distance_weight
        car_from_score = bill.from_route.car_distance.total_seconds() * weights.car_from_distance_weight
        public_from_score = bill.from_route.public_transport_distance.total_seconds() * weights.public_from_transport_distance_weight
        
        return price_score + time_score + walk_to_score  + car_to_score + public_to_score + walk_from_score  + car_from_score + public_from_score
        
    
    def optimize(self, bills: list[Bill], weights: SearchWeights):
        scores = [self.score_bill(bill, weights) for bill in bills]
        scores, bills = zip(*sorted(zip(scores, bills)))
        return bills
    
    def letter_search(self, input: LetterInput, weights: SearchWeights):
        return self.optimize([
            result for service in self.services for result in service.search_letter(input)
        ], weights)
    
    def box_search(self, input: BoxInput, weights: SearchWeights):
        return self.optimize([
            result for service in self.services for result in service.search_box(input)
        ], weights)