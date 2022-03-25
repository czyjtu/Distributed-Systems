import json
import datetime
from pathlib import Path
import warnings
from app.analyzer import OffersAnalyzer


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f)


def save_response(response, path: Path):
    timestamp = datetime.datetime.now()
    fname = timestamp.strftime("%H_%M_%S")
    try:
        save_json(response.json(), path / (fname + ".json"))
    except Exception as e:
        warnings.warn(f"Cannot save given response in .json due to error: {e}")
        with open(path / (fname + ".txt"), "w") as f:
            f.write(response.text())

def prepare_response(analyzer: OffersAnalyzer) -> dict:
    response = {
        "num_offers": len(analyzer._df),
        "salary": {
            "min_mean": analyzer.salary_mean[0],
            "max_mean": analyzer.salary_mean[1],
            "min_std": analyzer.salary_std[0],
            "max_std": analyzer.salary_std[1],
            "extreme": f"{analyzer.salary_extreme[0]} - {analyzer.salary_extreme[1]}",
        },
        "word_list": [
            f"{word} #{count}" for word, count in analyzer.common_words
        ],
    }
    return response