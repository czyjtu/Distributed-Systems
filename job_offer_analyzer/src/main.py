from fastapi import FastAPI
from pprint import pformat
from app.external.reed import ReedOffers
from app.external.base import IOfferGetter
from app.models.query_data import QueryData
from app.analyzer import OffersAnalyzer
from app.config import CONFIG

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
    print(CONFIG['reed_api_key'])

if __name__ == '__main__':
    main()