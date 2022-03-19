from fastapi import FastAPI
from app.external.reed import ReedOffers
from app.external.base import IOfferGetter
from app.models.query_data import JobType, QueryData
from app.analyzer import OffersAnalyzer
from app.config import CONFIG
from pprint import pprint

API_LIST: list[IOfferGetter] = [ReedOffers()]

app = FastAPI()


@app.get("/")
async def root(query: QueryData):
    offers = list(map(lambda api: api.get_offers(query), API_LIST))
    analyzer = OffersAnalyzer(offers)

    response = {
        "mean_salary": analyzer.mean_salary,
        "common_words": analyzer.common_words,
    }

    return response


def main():
    query = QueryData(query="python", location="London", job_type=JobType.FULL_TIME)
    for api in API_LIST:
        pprint(api.get_offers(query))


if __name__ == "__main__":
    main()
