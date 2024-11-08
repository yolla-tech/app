from fastapi import FastAPI

from models.input import LetterInput, BoxInput
from models.output import Bill
from models.search_weights import SearchWeights

from services.cargo_search_manager import CargoSearchManager, SearchWeights
from services.cargo_services.scrapper_service import ScrapperService

app = FastAPI()

controller = CargoSearchManager(services=[
    ScrapperService()
])

@app.post("/search_letter")
def search_letter(letter: LetterInput, weights: SearchWeights) -> list[Bill]:
    return controller.letter_search(letter, weights)

@app.post("/search_box")
def search_box(box: BoxInput, weights: SearchWeights) -> list[Bill]:
    return controller.box_search(box, weights)

