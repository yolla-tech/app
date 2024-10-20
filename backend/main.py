from fastapi import FastAPI

from models.input import LetterInput, BoxInput
from models.output import Bill

from services.controller import SearchController, SearchWeights
from services.base import generate_random_services

app = FastAPI()

controller = SearchController(services=generate_random_services(10))

@app.post("/search_letter")
def search_letter(letter: LetterInput) -> list[Bill]:
    weights = SearchWeights(price_weight=0.6, time_weight=0.1, walk_weight=0.1, public_weight=0.1, car_weight=0.1)
    return controller.letter_search(letter, weights)

@app.post("/search_box")
def search_box(box: BoxInput) -> list[Bill]:
    weights = SearchWeights(price_weight=0.6, time_weight=0.1, walk_weight=0.1, public_weight=0.1, car_weight=0.1)
    return controller.box_search(box, weights)

