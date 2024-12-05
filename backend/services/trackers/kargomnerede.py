from services.trackers.base import StatusTracker
from models.tracker import TrackedPackage, TrackedPackageMovement

import requests
import re


class KargomNeredeStatusTracker(StatusTracker):
    __url: str

    def __init__(self) -> None:
        self.__url = "https://kargom-nerede.p.rapidapi.com/tracking/"
        self.__company_id_to_name_mapping = {
            1: 'Aras Kargo',
            2: 'Yurtiçi Kargo',
            6: 'Sürat Kargo',
            4: 'PTT Kargo',
            3: 'MNG Kargo',
            10: 'HepsiJet',
            9: 'Trendyol Express',
            5: 'UPS Kargo',
            15: 'Kolay Gelsin',
            37: 'KargomSende',
            25: 'Jetizz',
            29: 'Aras Kurye',
            24: 'KargoIst',
            27: 'Aramex',
            2224: 'YunExpress'
        }
        self.__company_name_to_id_mapping = {
            v: k for k, v in self.__company_id_to_name_mapping.items()}
        self.__cammel_to_snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')

    def __get__company_id_from_name(self, company_id: int) -> str:
        return self.__company_id_to_name_mapping[company_id]

    def __get__company_name_from_id(self, name: str) -> int:
        return self.__company_name_to_id_mapping[name]

    def __cammel_to_snake(self, s: str) -> str:
        return self.__cammel_to_snake_case_pattern.sub('_', s).lower()

    def __get_status(self, tracking_code: str, compony_id: int):
        url = "https://kargom-nerede.p.rapidapi.com/tracking"
        payload = {
            "code": "4460068108558",
            "companyId": 1
        }
        headers = {
            "x-rapidapi-key": "58aa0501d8msh7afe362fe683735p12f7fcjsna92abf6a60a7",
            "x-rapidapi-host": "kargom-nerede.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(response.status_code, response.content)
            return None

        data: dict = response.json()

        data = {self.__cammel_to_snake(key): value for key, value in data['value'].items()}
        
        data['movement'] = [{self.__cammel_to_snake(key): value for key, value in movement.items()} for movement in data['movement']]

        return TrackedPackage.model_validate(data)



    def get_status_by_name(self, tracking_code: str, company: str):
        return self.__get_status(
            tracking_code=tracking_code,
            compony_id=self.__get__company_name_from_id(company)
        )


    def get_status_by_id(self, tracking_code: str, company_id: int):
        return self.__get_status(
            tracking_code=tracking_code,
            compony_id=company_id
        )
        
    
    def get_companies(self):
        return self.__company_id_to_name_mapping