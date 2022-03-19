from fastapi import FastAPI
from app.external.reed import ReedOffers
from app.external.base import IOfferGetter
from app.models.query_data import JobType, QueryData
from app.analyzer import OffersAnalyzer
from app.config import CONFIG
from pprint import pprint
import itertools as it 

API_LIST: list[IOfferGetter] = [ReedOffers()]

app = FastAPI()


@app.get("/analyze")
async def root(keywords: str, location: str):
    query = QueryData(query=keywords, location=location, job_type=JobType.FULL_TIME)
    offers = list(it.chain.from_iterable(map(lambda api: api.get_offers(query), API_LIST)))
    analyzer = OffersAnalyzer(offers)

    response = {
        "salary": {
            "min mean": analyzer.salary_mean[0],
            "max mean": analyzer.salary_mean[1],
            "min std": analyzer.salary_std[0],
            "max std": analyzer.salary_std[1],
            "extreme": f"{analyzer.salary_extreme[0]} - {analyzer.salary_extreme}"
        },
        "most common words": [f"{word} #{count}" for word, count in analyzer.common_words],
    }
    return response


def main():
    query = QueryData(query="python machine learning", location="London", job_type=JobType.FULL_TIME)
    
    offers = []
    for api in API_LIST:
        offers += api.get_offers(query)

    analyzer = OffersAnalyzer(offers)
    print(analyzer.salary_mean, analyzer.salary_std, analyzer.common_words)
    analyzer._df.to_csv("test.csv")
    analyzer.common_words.to_csv("count.csv")

if __name__ == "__main__":
    main()
