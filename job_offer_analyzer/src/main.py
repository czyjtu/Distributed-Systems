from fastapi import FastAPI, Form, Request
from app.exceptions import ResponseStatusError
from app.external.reed import ReedOffers
from app.external.base import IOfferGetter
from app.models.query_data import JobType, QueryData
from app.analyzer import OffersAnalyzer
from app.config import CONFIG
import itertools as it
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from aiohttp.client_exceptions import ClientConnectionError
from app.utils import prepare_response

API_LIST: list[IOfferGetter] = [ReedOffers()]

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/analyze", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "response": {"salary": ""}})


@app.post("/analyze", response_class=HTMLResponse)
async def root(
    request: Request,
    keywords: str = Form(''),
    location: str = Form(''),
    part_time: bool = Form(False)
):
    query = QueryData(
        query=keywords,
        location=location,
        job_type=(JobType.FULL_TIME if not part_time else JobType.PART_TIME),
    )
    print(query)
    # offers = list(
    #     it.chain.from_iterable(map(lambda api: api.get_offers(query), API_LIST))
    # )
    try:
        offers = await API_LIST[0].get_offers(query)
    except ClientConnectionError as e:
        return e
    except ResponseStatusError as e:
        if e.status == 401:
            return f"Canot connect to the reed client due to invalid api key"
        elif e.status == 403:
            return f"per-hour request limit was exceeded"
        return f"Failed to connect to reed api. Got status {e.status}"

    if len(offers) == 0:
        return "no job offers was found"
    analyzer = OffersAnalyzer(offers)
    response = prepare_response(analyzer)
    return templates.TemplateResponse(
        "form.html", {"request": request, "response": response}
    )
