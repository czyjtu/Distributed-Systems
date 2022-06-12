from abc import ABC, abstractmethod
from app.models import QueryData, JobOffer

class IOfferGetter(ABC):
    @abstractmethod
    def get_offers(form: QueryData) -> list[JobOffer]:
        pass