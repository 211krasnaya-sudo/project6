from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAPI(ABC):
    """Базовый класс для работы с внешними API."""

    @abstractmethod
    def get_country_bbox(self, country_name: str) -> Optional[Dict[str, float]]:
        """Возвращает bounding box страны (south, north, west, east) или None."""
        pass

    @abstractmethod
    def get_aircrafts_in_bbox(
        self,
        south: float,
        north: float,
        west: float,
        east: float
    ) -> list[Dict[str, Any]]:
        """Возвращает список самолётов в прямоугольнике координат."""
        pass