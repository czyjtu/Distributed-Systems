from app import ROOT_PATH
from app.external.base import IOfferGetter
from app.utils import save_response
from app.models import JobOffer, QueryData, JobType
from app.config import CONFIG
from http import HTTPStatus
from pydantic.error_wrappers import ValidationError
import requests


class ReedOffers(IOfferGetter):
    def __init__(self):
        self._api_key = CONFIG["reed"]["api_key"]
        self.base_url = CONFIG["reed"]["base_url"]
        self.max_results = CONFIG["reed"]["max_results"]

    def get_offers(self, query: QueryData) -> list[JobOffer]:
        url = self._job_search_url(query)
        response_json = self._get_response(url, save=True)
        # result = self._process_response(response_json)
        details = list(
            map(
                lambda o: self._get_response(self._job_details_url(o["jobId"])),
                response_json["results"],
            )
        )
        offers = list(map(self._build_job_offer, details))
        # skip offers with missing data 
        offers = list(filter(None, offers))
        return offers

    def _get_response(self, url, save=False):
        response = requests.get(url, auth=(self._api_key, None))
        assert (
            response.status_code == HTTPStatus.OK
        ), f"Invalid status code {response.status_code} {response.content}"
        if save:
            save_response(response, ROOT_PATH.parent / "data/reed")
        return response.json()

    def _process_response(self, response: dict) -> list[JobOffer]:
        offers = []
        for offer_dict in response["results"]:
            try:
                offer = JobOffer(
                    description=offer_dict["jobDescription"],
                    salary_lb=offer_dict["minimumSalary"],
                    salary_ub=offer_dict["maximumSalary"],
                    title=offer_dict["jobTitle"],
                )
            except ValidationError as e:
                print("skipped job offer due to validation error")
                continue
            offers.append(offer)

        return offers

    def _build_job_offer(self, offer_dict):
        try:
            offer = JobOffer(
                description=offer_dict["jobDescription"],
                salary_lb=offer_dict["minimumSalary"],
                salary_ub=offer_dict["maximumSalary"],
                salary_type=offer_dict["salaryType"],
                currency=offer_dict["currency"],
                title=offer_dict["jobTitle"],
                employer=offer_dict["employerName"],
            )
        except ValidationError as e:
            print("skipped job offer due to validation error")
            return None
        return offer

    def _job_search_url(self, query: QueryData) -> str:
        is_part_time = query.job_type == JobType.PART_TIME
        is_full_time = query.job_type == JobType.FULL_TIME
        params = (
            f"?keywords={query.query}"
            f"&location={query.location}"
            f"&partTime={is_part_time}"
            f"&fullTime={is_full_time}"
            f"&resultsToTake={self.max_results}"
        )
        return self.base_url + "search" + params

    def _job_details_url(self, job_id) -> str:
        return self.base_url + f"jobs/{job_id}"
