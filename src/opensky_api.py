import requests
from typing import List, Dict, Any
from .api_base import BaseAPI

OPENS_KY_URL = "https://opensky-network.org/api/states/all"

class OpenSkyAPI(BaseAPI):
    def __init__(self):
        self.session = requests.Session()

    def get_country_bbox(self, country_name: str) -> None:
        # OpenSky не умеет искать страны, поэтому этот метод не реализуем.
        raise NotImplementedError("OpenSkyAPI не поддерживает поиск по названию страны.")

    def get_aircrafts_in_bbox(
        self,
        south: float,
        north: float,
        west: float,
        east: float
    ) -> List[Dict[str, Any]]:
        params = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east,
        }
        resp = self.session.get(OPENS_KY_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        states = data.get("states", [])
        # states — это список списков, где индексы фиксированы.
        # Документация OpenSky: https://openskynetwork.github.io/opensky-api/rest.html
        return [
            {
                "icao24": row[0],
                "callsign": row[1].strip() if row[1] else "",
                "origin_country": row[2].strip() if row[2] else "",
                "time_position": row[3],
                "last_contact": row[4],
                "longitude": row[5],
                "latitude": row[6],
                "baro_altitude": row[7],
                "on_ground": row[8],
                "velocity": row[9],
                "true_track": row[10],
                "vertical_rate": row[11],
                "sensors": row[12],
                "geo_altitude": row[13],
                "squawk": row[14],
                "spi": row[15],
                "position_source": row[16],
            }
            for row in states
        ]