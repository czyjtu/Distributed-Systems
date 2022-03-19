from app.models import JobOffer
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

try:
    nltk.data.find("wordnet")
except LookupError:
    nltk.download("wordnet")
try:
    nltk.data.find('omw-1.4')
except LookupError:
    nltk.download('omw-1.4')


class OffersAnalyzer:
    def __init__(self, offers: list[JobOffer]):
        self.offers = offers
        self._df = pd.DataFrame([dict(o) for o in offers])

        # stats placeholders
        self._mean_salary = None
        self._words_counter = None

        # text preprocessing utils
        self._lemmatizer = WordNetLemmatizer()
        self._stop = stopwords.words("english")

    @property
    def mean_salary(self) -> tuple[int, int]:
        if self._mean_salary is None:
            self._mean_salary = self.get_salary_mean()
        return self._mean_salary

    @property
    def common_words(self):
        if self._words_counter is None:
            self._words_counter = self.get_words_histogram()
        return self._words_counter  # [word for word, _ in self._words_counter[:20]]

    def get_salary_mean(self):
        return self._df["salary_lb"].mean(), self._df["salary_ub"].mean()

    def get_salary_std(self):
        return self._df["salary_lb"].std(), self._df["salary_ub"].std()

    def get_words_histogram(self):
        self._description_preprocessing()
        return self._df['description'].str.split(expand=True).stack().value_counts()

    def _description_preprocessing(self):
        self._df["description"] = self._df["description"].apply(lambda x: x.lower())
        self._df["description"] = self._df["description"].str.replace("[^ \w\s]", " ")
        self._df["description"] = self._df["description"].str.replace("\d+", "")

        self._df["description"] = self._df["description"].apply(
            lambda x: " ".join(x for x in x.split() if x not in self._stop)
        )
        self._df["description"] = self._df["description"].apply(
            lambda x: " ".join([self._lemmatizer.lemmatize(word) for word in x.split()])
        )
