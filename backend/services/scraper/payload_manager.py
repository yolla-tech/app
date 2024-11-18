from services.scraper.data_manager import ScrapperDataManager
from services.scraper.exceptions import ScrapperPayloadValidationException, ScrapperException
from models.scraper_payload import Payload


class ScrapperPayloadManager:
    def __init__(self) -> None:
        self.__payload: dict = None
    
    def set_scrapper_data(self, scrapper_data: ScrapperDataManager) -> None:
        self.scrapper_data = scrapper_data
    
    def set_payload(self, payload: Payload) -> None:
        
        if payload.type != "letter" and payload.type != "box":
            raise ScrapperPayloadValidationException(f"Type must be either letter or box: {payload.type}")
    
        if payload.type == "box" and (payload.weight is None or payload.width is None or payload.length is None):
            raise ScrapperPayloadValidationException(f"Box must have weight, width, and height: Type->{payload.type} Width->{payload.width} Height->{payload.height} Length->{payload.length}")

        city_a: int = self.scrapper_data.cities.get(payload.city_a.lower())
        
        if city_a is None:
            raise ScrapperPayloadValidationException(f"Could not find city a: {payload.city_a}")
        
        city_b: int = self.scrapper_data.cities.get(payload.city_b.lower())
        
        if city_a is None:
            raise ScrapperPayloadValidationException(f"Could not find city a: {payload.city_a}")

        self.__payload = {
            "sehira": city_a,
            "sehirb": city_b,
            "agirlik": payload.weight,
            "en": payload.width,
            "boy": payload.length,
            "yukseklik": payload.height,
        }
    
        if payload.from_address:
            self.__payload["adrestenalim"] = "E"
        
        if payload.to_address:
            self.__payload["adreseteslim"] = "E"
            
        if payload.type == "letter":
            self.__payload["gonderituru"] = "D"
    
    def get_payload(self) -> dict[str, str | float]:
        if self.__payload is None:
            raise ScrapperException("ScrapperPayloadManager.set_payload must be called before ScrapperPayloadManage.get_payload")
        return self.__payload
