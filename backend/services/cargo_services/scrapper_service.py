from models.input import BaseInput, BoxProperties
from models.output import Bill, BillItem, Route
from models.scraper_payload import Payload

from services.cargo_services.base import BaseService
from services.scraper.scraper import Scrapper


class ScrapperService(BaseService):
    def __init__(self) -> None:
        self.scrapper = Scrapper()
        
    def __create_payload(self, input: BaseInput, from_address: bool, to_address: bool):
        input_type = "box" if self.is_box_search(input) else "letter"
        box_properties: BoxProperties = input.properties if self.is_box_search(input) else None
        
        return Payload(
            city_a=input.location_a,
            city_b=input.location_b,
            type=input_type,
            weight=box_properties.weight if box_properties else None,
            width=box_properties.width if box_properties else None,
            height=box_properties.height if box_properties else None,
            length=box_properties.length if box_properties else None,
            from_address=from_address,
            to_address=to_address
        )
        
    def __create_payloads(self, input: BaseInput) -> dict[str, Payload]:
        return {
            'standart': self.__create_payload(input=input, from_address=False, to_address=False),
            'from_address': self.__create_payload(input=input, from_address=True, to_address=False),
            'to_address': self.__create_payload(input=input, from_address=False, to_address=True),
            'from_and_to_address': self.__create_payload(input=input, from_address=True, to_address=True),
        }
    
    def __get_bill_for_service(self, service_name: str, service_type: str, data: dict[str, float]) -> Bill:
        items: list[BillItem] = [
            BillItem(name="Package", price=data['standart'])
        ]
        
        if "from" in service_type:
            items.append(BillItem(name="From Address", price=data['from_address'] - data['standart']))
            
        if "to" in service_type:
            items.append(BillItem(name="To Address", price= data['to_address'] - data['standart']))
        
        
        total = sum((i.price for i in items))
        return Bill(
            service_name=service_name,
            items=items,
            total_price=total,
            expected_time=None,
            from_address="from" in service_type,
            to_address="to" in service_type,
            from_route=Route(),
            to_route=Route(),
        )
        
    def __get_bills_for_service(self, service_name: str, data: dict[str, float]) -> list[Bill]:
        return [self.__get_bill_for_service(service_name, service_type, data) for service_type in data.keys()]
        
    def search(self, input: BaseInput) -> list[Bill]:
        payloads: dict[str, Payload] = self.__create_payloads(input)
        scrapped_results = {k: self.scrapper.scrap_data(v) for k, v in payloads.items()}
        transformed_data = {
            service: {service_type: services[service] for service_type, services in scrapped_results.items()}
            for service in next(iter(scrapped_results.values()))
        }
        return [bill for service, data in transformed_data.items() for bill in self.__get_bills_for_service(service, data)]