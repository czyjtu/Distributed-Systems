from app import ROOT_PATH
from app.external.base import IOfferGetter
from app.external.utils import save_response
from app.models import JobOffer, QueryData, JobType
from app.config import CONFIG
import requests


class ReedOffers(IOfferGetter):
    def __init__(self):
        self._api_key = CONFIG["reed"]["api_key"]
        self.base_url = CONFIG["reed"]["base_url"]
        self.max_results = CONFIG["reed"]["max_results"]

    def get_offers(self, query: QueryData) -> list[JobOffer]:
        url = self._build_url(query)

        response = requests.get(url, auth=(self._api_key, None))
        save_response(response, ROOT_PATH.parent / "data/reed")

        result = response.text
        return result

    def _build_url(self, query: QueryData) -> str:
        is_part_time = query.job_type == JobType.PART_TIME
        is_full_time = query.job_type == JobType.FULL_TIME
        params = (
            f"?keywords={query.query}"
            f"&location={query.location}"
            f"&partTime={is_part_time}"
            f"&fullTime={is_full_time}"
        )
        return self.base_url + "search" + params