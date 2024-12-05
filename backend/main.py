from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from models.input import LetterInput, BoxInput, TrackByNameInput, TrackByIdInput
from models.output import Bill
from models.search_weights import SearchWeights
from models.register_user import RegisterUserModel
from models.login_user import LoginUserModel

from services.cargo_search_manager import CargoSearchManager, SearchWeights
from services.cargo_services.scrapper_service import ScrapperService
from services.scraper.exceptions import ScrapperPayloadValidationException, ScrapperException
from services.trackers.kargomnerede import KargomNeredeStatusTracker

from db.session import get_db

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://0.0.0.0:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

controller = CargoSearchManager(services=[
    ScrapperService()
])

tracker = KargomNeredeStatusTracker()

@app.post("/search_letter")
def search_letter(letter: LetterInput, weights: SearchWeights) -> list[Bill]:
    try:
        return controller.letter_search(letter, weights)
    except ScrapperPayloadValidationException as e:
        raise HTTPException(422, detail=f"Payload validation error: {e}")
    except ScrapperException as e:
        raise HTTPException(500, detail=f"Scrapper server error: {e}")    

@app.post("/search_box")
def search_box(box: BoxInput, weights: SearchWeights) -> list[Bill]:
    try:
        return controller.box_search(box, weights)
    except ScrapperPayloadValidationException as e:
        raise HTTPException(422, detail=f"Payload validation error: {e}")
    except ScrapperException as e:
        raise HTTPException(500, detail=f"Scrapper server error: {e}")


@app.post("/register")
def register(user: RegisterUserModel, db: Session = Depends(get_db)):
    ...
    
@app.post("/login")
def login(user: LoginUserModel, db: Session = Depends(get_db)):
    ...


@app.post("/track_by_name")
def track_by_name(input: TrackByNameInput):
    return tracker.get_status_by_name(
        tracking_code=input.tracking_code,
        company=input.company_name
    )
    

@app.post("/track_by_id")
def track_by_id(input: TrackByIdInput):
    return tracker.get_status_by_id(
        tracking_code=input.tracking_code,
        company_id=input.company_id
    )
    
    

@app.get("/tacked_companies")
def tracked_companies():
    return tracker.get_companies()