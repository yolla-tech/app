from services.trackers.base import StatusTracker

import requests

class KargomNeredeStatusTracker(StatusTracker):
    __url: str
    
    def __init__(self) -> None:
        self.__url = "https://kargom-nerede.p.rapidapi.com/tracking" 
    
    def __get_status(self, tracking_code: str, compony_id: int):
        response = requests.post(
            url=self.__url, 
            headers={
                "Content-Type": "application/json",
                "x-rapidapi-host": "kargom-nerede.p.rapidapi.com",
                "x-rapidapi-key": "58aa0501d8msh7afe362fe683735p12f7fcjsna92abf6a60a7"
            },
            data={
                "code": tracking_code,
                "companyId": compony_id
            }
        )
        if response.status_code != 200:
            return None
        print(response)
        
    
    def get_status(self, tracking_code: str, company_id: int):
        return self.__get_status(
            tracking_code=tracking_code,
            compony_id=company_id
        )