from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.input import LetterInput, BoxInput
from models.output import Bill
from models.search_weights import SearchWeights

from services.cargo_search_manager import CargoSearchManager, SearchWeights
from services.cargo_services.scrapper_service import ScrapperService
from services.scraper.exceptions import ScrapperPayloadValidationException, ScrapperException

app = FastAPI()

origins = [
    "https://yolla.tech",
    "https://www.yolla.tech",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["Content-Type", "Authorization"]
)

controller = CargoSearchManager(services=[
    ScrapperService()
])

@app.get("/")
async def root():
    return {"message": "CORS is configured!"}

@app.post("/api/search_letter")
def search_letter(letter: LetterInput, weights: SearchWeights) -> list[Bill]:
    try:
        return controller.letter_search(letter, weights)
    except ScrapperPayloadValidationException as e:
        raise HTTPException(422, detail=f"Payload validation error: {e}")
    except ScrapperException as e:
        raise HTTPException(500, detail=f"Scrapper server error: {e}")    

@app.post("/api/search_box")
def search_box(box: BoxInput, weights: SearchWeights) -> list[Bill]:
    try:
        return controller.box_search(box, weights)
    except ScrapperPayloadValidationException as e:
        raise HTTPException(422, detail=f"Payload validation error: {e}")
    except ScrapperException as e:
        raise HTTPException(500, detail=f"Scrapper server error: {e}")
