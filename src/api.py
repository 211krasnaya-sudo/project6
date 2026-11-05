"""Работа с API Nominatim и OpenSky Network."""
from abc import ABC, abstractmethod
from typing import Any, Optional

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPENSKY_URL = "https://opensky-network.org/api/states/all"


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_coordinates(self, country: str) -> Optional[dict[str, float]]:
        """Вернуть boundingbox страны: юг, север, запад, восток."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[dict[str, Any]]:
        """Вернуть список самолётов в воздушном пространстве страны."""


class AeroplanesAPI(BaseAPI):
    """Реализация работы с Nominatim и OpenSky Network."""

    def __init__(self, user_agent: str = "aircraft_tracker") -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def get_coordinates(self, country: str) -> Optional[dict[str, float]]:
        """Получить boundingbox страны через Nominatim."""
        try:
            response = self.session.get(
                NOMINATIM_URL,
                params={"q": country, "format": "json", "limit": 1},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as error:
            print(f"Ошибка запроса к Nominatim: {error}")
            return None

        if not data:
            return None
        bbox = data[0].get("boundingbox")
        if not bbox or len(bbox) != 4:
            return None
        south, north, west, east = map(float, bbox)
        return {"south": south, "north": north,
                "west": west, "east": east}

    def get_aeroplanes(self, country: str) -> list[dict[str, Any]]:
        """Получить самолёты в воздушном пространстве страны."""
        bbox = self.get_coordinates(country)
        if bbox is None:
            return []
        try:
            response = self.session.get(
                OPENSKY_URL,
                params={
                    "lamin": bbox["south"],
                    "lamax": bbox["north"],
                    "lomin": bbox["west"],
                    "lomax": bbox["east"],
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as error:
            print(f"Ошибка запроса к OpenSky: {error}")
            return []

        return self._parse_states(payload.get("states") or [])

    @staticmethod
    def _parse_states(states: list) -> list[dict[str, Any]]:
        """Преобразовать ответ OpenSky в список словарей."""
        keys = [
            "icao24", "callsign", "origin_country", "time_position",
            "last_contact", "longitude", "latitude", "baro_altitude",
            "on_ground", "velocity", "true_track", "vertical_rate",
            "sensors", "geo_altitude", "squawk", "spi", "position_source",
        ]
        result = []
        for row in states:
            entry = dict(zip(keys, row))
            if entry.get("callsign"):
                entry["callsign"] = entry["callsign"].strip()
            result.append(entry)
        return result
