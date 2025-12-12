import json
from pathlib import Path

SETTINGS_PATH = Path("data/settings.json")


def load_settings():
    if not SETTINGS_PATH.exists():
        return None

    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(data: dict):
    SETTINGS_PATH.parent.mkdir(exist_ok=True)

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
