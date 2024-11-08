from bs4 import BeautifulSoup
from bs4.element import Tag
import math

from services.scraper.data_manager import ScrapperDataManager
from services.scraper.payload_manager import ScrapperPayloadManager
from models.scraper_payload import Payload

class Scrapper:
    def __init__(self) -> None:
        self.scrapper_data = ScrapperDataManager()
        self.payload_manager = ScrapperPayloadManager()
        self.payload_manager.set_scrapper_data(self.scrapper_data)
        
    @staticmethod
    def __format_html(contents: list) -> dict[str, float]:
            results = []

            i = 0
            while i < len(contents):
                element = contents[i]
                
                # Check if the element is a <b> tag (service name)
                if isinstance(element, Tag) and element.name == 'b':
                    service_name = element.get_text(strip=True)
                    
                    # Check if this is the 'NOT' section
                    if service_name == 'NOT:':
                        # Extract the note text
                        note_text = contents[i + 1].strip()
                        break  # Exit the loop after handling the note
                    else:
                        # Get the price info from the next element
                        price_info = contents[i + 1].strip()
                        # Append the service name and price to the results list
                        results.append({'service': service_name, 'price': price_info})
                        i += 2  # Skip the <br/> tag
                i += 1  # Move to the next element
            
            services = {}

            for item in results:
                name = item['service'].split()[0]
                price = float(item['price'].split()[0].replace(',', '.'))
                services[name] = min(services.get(name, math.inf), price)
            
            return services
    
    def scrap_data(self, payload: Payload) -> dict[str, float]:
        self.payload_manager.set_payload(payload=payload)

        response = self.scrapper_data.session.post(
            self.scrapper_data.url, 
            headers=self.scrapper_data.headers, 
            data=self.payload_manager.get_payload(), 
            cookies=self.scrapper_data.cookies
        )
        
        if response.status_code != 200:
            raise Exception(f"Failure, status code: {response.status_code}")
        
        soup2 = BeautifulSoup(response.content, "html.parser")
        return self.__format_html(soup2.find("div", {"id": "hsonuc"}).contents)