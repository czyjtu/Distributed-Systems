from fastapi import FastAPI, Form, Request
from app.external.reed import ReedOffers
from app.external.base import IOfferGetter
from app.models.query_data import JobType, QueryData
from app.analyzer import OffersAnalyzer
from app.config import CONFIG
import itertools as it
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.utils import prepare_response
 
API_LIST: list[IOfferGetter] = [ReedOffers()]

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/analyze", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def root(request: Request, keywords: str = Form(None), location: str = Form(None), part_time: bool = Form(False)):
    query = QueryData(query=keywords, location=location, job_type=(JobType.FULL_TIME if not part_time else JobType.PART_TIME))
    offers = list(
        it.chain.from_iterable(map(lambda api: api.get_offers(query), API_LIST))
    )
    analyzer = OffersAnalyzer(offers)
    response = prepare_response(analyzer)
    return templates.TemplateResponse("form.html", {"request": request, "response": response})

