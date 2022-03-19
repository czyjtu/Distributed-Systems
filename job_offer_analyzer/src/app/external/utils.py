import json
import datetime
from pathlib import Path
import warnings


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
            f.write(response.text)