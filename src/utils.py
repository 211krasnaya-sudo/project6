import requests
from typing import Optional, Dict
from .api import BaseAPI

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

class NominatimAPI(BaseAPI):
    def __init__(self, user_agent: str = "aircraft_tracker"):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get_country_bbox(self, country_name: str) -> Optional[Dict[str, float]]:
        params = {
            "q": country_name,
            "format": "json",
            "limit": 1,
            "countrycodes": ""  # чтобы искать по названию страны
        }
        resp = self.session.get(NOMINATIM_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            return None

        result = data[0]
        bbox_str = result.get("boundingbox")
        if not bbox_str:
            return None

        # boundingbox: ["south", "north", "west", "east"]
        try:
            south, north, west, east = map(float, bbox_str)
            return {"south": south, "north": north, "west": west, "east": east}
        except (ValueError, TypeError):
            return None

    def get_aircrafts_in_bbox(self, south: float, north: float, west: float, east: float) -> list[dict]:
        # Этот метод здесь не используется напрямую: за самолёты отвечает OpenSky.
        # Но он нужен, чтобы удовлетворить интерфейс BaseAPI.
        return []