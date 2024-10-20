from datetime import datetime

from models.output import Bill
from models.input import LetterInput, BoxInput
from services.base import BaseService

class SearchWeights:
    def __init__(
        self, 
        price_weight: float, 
        time_weight: float, 
        walk_weight: float, 
        public_weight: float, 
        car_weight: float) -> None:
        
        self.price_weight = price_weight
        self.time_weight = time_weight
        self.walk_distance_weight = walk_weight
        self.public_transport_distance_weight = public_weight
        self.car_distance_weight = car_weight
    

class SearchController:
    def __init__(self, services: list[BaseService] = []) -> None:
        self.services = services
    
    def score_bill(self, bill: Bill, weights: SearchWeights) -> float:
        price_score = bill.total_price * weights.price_weight
        time_score = bill.expected_time.timestamp() * weights.time_weight
        walk_score = (bill.to_route.walk_distance + bill.from_route.walk_distance).total_seconds() * weights.walk_distance_weight
        car_score = (bill.to_route.car_distance + bill.from_route.car_distance).total_seconds() * weights.car_distance_weight
        public_score = (bill.to_route.public_transport_distance + bill.from_route.public_transport_distance).total_seconds() * weights.public_transport_distance_weight
        return price_score + time_score + walk_score  + car_score + public_score
        
    
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