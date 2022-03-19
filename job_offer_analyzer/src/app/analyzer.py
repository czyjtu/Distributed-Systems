from app.models import JobOffer


class OffersAnalyzer:
    def __init__(self, offers: list[JobOffer]):
        self.offers = offers

    @property
    def mean_salary(self):
        if self._mean_salary is None:
            self._mean_salary = self.get_mean_salary()
        return self._mean_salary

    @property
    def common_words(self):
        if self._words_counter is None:
            self._words_counter = self.get_words_histogram()
        return [word for word, _ in self._words_counter[:20]]

    def get_mean_salary(self):
        raise NotImplementedError

    def get_words_histogram(self):
        raise NotImplementedError
