from app.external.base import IOfferGetter
from app.models.job_offer import JobOffer
from app.models.query_data import QueryData 

class ReedOffers(IOfferGetter):
    def __init__(self):
        self.user_id = ...

    def get_offers(self, query: QueryData) -> list[JobOffer]:
        raise NotImplementedError

    def _build_request(self, query: QueryData) -> str:
        raise NotImplementedError