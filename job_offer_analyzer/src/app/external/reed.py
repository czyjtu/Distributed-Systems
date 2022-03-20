from app import ROOT_PATH
from app.exceptions import ResponseStatusError
from app.external.base import IOfferGetter
from app.utils import save_response
from app.models import JobOffer, QueryData, JobType
from app.config import CONFIG
from http import HTTPStatus
from pydantic.error_wrappers import ValidationError

import aiohttp
import asyncio


class ReedOffers(IOfferGetter):
    def __init__(self):
        self._api_key = CONFIG["reed"]["api_key"]
        self._auth = aiohttp.BasicAuth(self._api_key)
        self.base_url = CONFIG["reed"]["base_url"]
        self.max_results = CONFIG["reed"]["max_results"]

    async def get_offers(self, query: QueryData) -> list[JobOffer]:
        search_url = self._job_search_url(query)
        async with aiohttp.ClientSession(auth=self._auth) as session:
            offers_json = await self._get_response(session, search_url)
            offers_ids = [o["jobId"] for o in offers_json["results"]]

            details_url = self.base_url + "jobs/{}"
            tasks = [
                asyncio.ensure_future(
                    self._get_response(session, details_url.format(job_id))
                )
                for job_id in offers_ids
            ]
            offers_details_jsons = await asyncio.gather(*tasks, return_exceptions=True)

        offers = [
            self._build_job_offer(o)
            for o in offers_details_jsons
            if isinstance(o, dict)  # skip exceptions
        ]
        # skip offers with missing data
        offers_filtered = list(filter(None, offers))
        return offers_filtered

    async def _get_response(self, session, url, save=False):
        async with session.get(url) as response:
            if response.status != HTTPStatus.OK:
                print(await response.text())
                raise ResponseStatusError(response.status)
            return await response.json()

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
