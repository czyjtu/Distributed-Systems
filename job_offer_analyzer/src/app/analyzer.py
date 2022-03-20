from __future__ import annotations
from app.models import JobOffer
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


try:
    nltk.data.find("wordnet")
except LookupError:
    nltk.download("wordnet")
try:
    nltk.data.find("omw-1.4")
except LookupError:
    nltk.download("omw-1.4")


class OffersAnalyzer:
    def __init__(self, offers: list[JobOffer]):
        self.offers = offers
        self._df = pd.DataFrame([dict(o) for o in offers])

        # stats placeholders
        self._mean_salary = None
        self._std_salary = None
        self._words_counter = None
        self._salary_extreme = None

        # text preprocessing utils
        self._lemmatizer = WordNetLemmatizer()
        self._ps = PorterStemmer()
        self._stop = stopwords.words("english") + other_stop_words
        self._stop += [self._ps.stem(word) for word in self._stop]
        self._stop = set(self._stop)
        self._salary_preprocessing()
        self._description_preprocessing()

    @property
    def salary_mean(self) -> tuple[int, int]:
        if self._mean_salary is None:
            self._mean_salary = int(self._df["salary_lb"].mean()), int(
                self._df["salary_ub"].mean()
            )
        return self._mean_salary

    @property
    def salary_std(self) -> tuple[int, int]:
        if self._std_salary is None:
            self._std_salary = self._df["salary_lb"].std(), self._df["salary_ub"].std()
        return self._std_salary

    @property
    def salary_extreme(self) -> tuple[int, int]:
        return int(self._df["salary_lb"].min()), int(self._df["salary_ub"].max())

    @property
    def common_words(self):
        if self._words_counter is None:
            self._words_counter = (
                self._df["description"].str.split(expand=True).stack().value_counts()
            )
        return list(self._words_counter.items())

    def _salary_preprocessing(self):
        self._df.drop(self._df[self._df.salary_type != "per annum"].index, inplace=True)

    def _description_preprocessing(self):
        self._df["description"] = self._df["description"].apply(lambda x: x.lower())
        self._df["description"] = self._df["description"].str.replace("<.*?>", " ")
        self._df["description"] = self._df["description"].str.replace("[^ \w\s]", " ")
        self._df["description"] = self._df["description"].str.replace("\d+", "")

        self._df["description"] = self._df["description"].apply(
            lambda x: " ".join([self._lemmatizer.lemmatize(word) for word in x.split()])
        )
        self._df["description"] = self._df["description"].apply(
            lambda x: " ".join(
                x for x in x.split() if self._ps.stem(x) not in self._stop
            )
        )
        # TODO: use sklearn and naive bayess to determine most important features


other_stop_words = [
    "job",
    "work",
    "company",
    "technique",
    "candidate",
    "skill",
    "years",
    "technology",
    "organization",
    "account",
    "manager",
    "scientist",
    "developer",
    "strong",
    "team",
    "software",
    "engineer",
    "looking",
    "stack",
    "benefit",
]
