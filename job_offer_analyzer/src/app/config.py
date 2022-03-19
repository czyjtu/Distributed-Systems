import json
from app import ROOT_PATH

CONFIG_FILENAME = "config.json"

with open(ROOT_PATH.parent / CONFIG_FILENAME, "r") as f:
    CONFIG = json.load(f)
