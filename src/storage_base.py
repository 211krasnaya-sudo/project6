from abc import ABC, abstractmethod
from typing import List
from .models import Aeroplane

class StorageBase(ABC):
    @abstractmethod
    def add_aeroplane(self, plane: Aeroplane) -> None:
        pass

    @abstractmethod
    def delete_aeroplane_by_callsign(self, callsign: str) -> bool:
        pass

    @abstractmethod
    def get_all(self) -> List[Aeroplane]:
        pass

    @abstractmethod
    def filter_by_country(self, country: str) -> List[Aeroplane]:
        pass