import json
from pathlib import Path
from typing import List
from .storage_base import StorageBase
from .models import Aeroplane

DATA_FILE = Path("data/aircrafts.json")

class JSONSaver(StorageBase):
    def __init__(self, filepath: Path = DATA_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.write_text("[]")

    def _load(self) -> list:
        with self.filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def _save(self, data: list) -> None:
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, plane: Aeroplane) -> None:
        data = self._load()
        # Проверка на дубли по callsign
        if any(row.get("callsign") == plane.callsign for row in data):
            return  # или можно выбросить исключение
        data.append({
            "callsign": plane.callsign,
            "origin_country": plane.origin_country,
            "velocity": plane.velocity,
            "baro_altitude": plane.baro_altitude,
            "icao24": plane.icao24,
            "latitude": plane.latitude,
            "longitude": plane.longitude,
        })
        self._save(data)

    def delete_aeroplane_by_callsign(self, callsign: str) -> bool:
        data = self._load()
        original_len = len(data)
        data = [row for row in data if row.get("callsign") != callsign]
        if len(data) < original_len:
            self._save(data)
            return True
        return False

    def get_all(self) -> List[Aeroplane]:
        raw = self._load()
        return Aeroplane.cast_to_object_list(raw)

    def filter_by_country(self, country: str) -> List[Aeroplane]:
        all_planes = self.get_all()
        country_lower = country.lower()
        return [p for p in all_planes if p.origin_country.lower() == country_lower]