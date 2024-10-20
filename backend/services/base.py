from abc import ABC

from models.input import BaseInput, LetterInput, BoxInput
from models.output import Bill, BillItem, Route

from datetime import datetime, timedelta

class BaseService(ABC):
    # should return at max 4 depending on the from and to services being availible
    def search(self, input: BaseInput, current_price: float) -> list[Bill]:
        ...
    
    def search_letter(self, letter_input: LetterInput):
        return self.search(letter_input, self.get_letter_price(letter_input))
    
    def search_box(self, box_input: BoxInput):
        return self.search(box_input, self.get_box_price(box_input))
    
    def get_to_address_price(self, input: BaseInput) -> float:
        ...
        
    def get_from_address_price(self, input: BaseInput) -> float:
        ...
        
    def get_letter_price(self, input: LetterInput) -> float:
        ...
    
    def get_box_price(self, input: BoxInput) -> float:
        ...



class TestService(BaseService):
    def __init__(
        self, 
        from_price: float, 
        to_price: float,
        letter_price: float, 
        box_price: float, 
        expected_time: datetime, 
        distance_by_car: timedelta) -> None:
        
        self.from_price = from_price
        self.to_price = to_price
        self.box_price = box_price
        self.letter_price = letter_price
        self.expected_time = expected_time
        self.distance_by_car = distance_by_car
    
    def get_letter_price(self, input: LetterInput) -> float:
        return self.letter_price
    
    def get_box_price(self, input: BoxInput) -> float:
        return self.box_price + input.properties.weight * 0.5
    
    def get_to_address_price(self, input: BaseInput) -> float:
        return self.to_price
        
    def get_from_address_price(self, input: BaseInput) -> float:
        return self.from_price
    
    def search(self, input: BaseInput, current_price: float) -> list[Bill]:
        def get_route(flag):
            return Route(
                    car_distance=self.distance_by_car * bool(not flag),
                    public_transport_distance=self.distance_by_car * 1.5 * bool(not flag),
                    walk_distance=self.distance_by_car * 2.0 * bool(not flag),
                )
        
        def get_items(from_address: bool, to_address: bool):
            items = [
                BillItem(name="Package", price=current_price),
            ]
            if from_address:
                items.append(BillItem(name="From Address",price=self.get_from_address_price(input)))
            if to_address:
                items.append(BillItem(name="To Address",price=self.get_to_address_price(input)))
            return items
        
        def get_bill(from_address: bool, to_address: bool):
            items = get_items(from_address, to_address)
            total = sum((i.price for i in items))
            return Bill(
                items=items,
                total_price=total,
                expected_time=self.expected_time,
                from_address=False,
                to_address=False,
                to_route=get_route(from_address),
                from_route=get_route(to_address)
            )
          
        return [
            get_bill(False, False),
            get_bill(False, True),
            get_bill(True, False),
            get_bill(True, True)
        ]

def generate_random_services(n):
    import random
    services = []
    for _ in range(n):
        from_price = round(random.uniform(10, 50), 2)
        to_price = round(random.uniform(50, 200), 2)
        letter_price = round(random.uniform(5, 20), 2)
        box_price = round(random.uniform(10, 100), 2)
        expected_time = datetime.now() + timedelta(days=random.randint(1, 10))
        distance_by_car = timedelta(hours=random.randint(1, 20))

        service = TestService(from_price, to_price, letter_price, box_price, expected_time, distance_by_car)
        services.append(service)
    
    return services
