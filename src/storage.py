"""Хранилища: абстрактный класс и JSON-коннектор."""
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union

from src.aeroplane import Aeroplane


class BaseSaver(ABC):
    """Абстрактное хранилище самолётов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить самолёт в хранилище."""

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> list[Aeroplane]:
        """Получить самолёты по критериям."""

    @abstractmethod
    def delete_aeroplane(
        self, aeroplane: Union[Aeroplane, str]
    ) -> bool:
        """Удалить самолёт. Возвращает True, если удалён."""


class JSONSaver(BaseSaver):
    """Хранение самолётов в JSON-файле."""

    def __init__(self, filepath: Path) -> None:
        self._filepath = filepath
        self._filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self._filepath.exists():
            self._filepath.write_text("[]", encoding="utf-8")

    def _connect(self) -> None:
        """Заглушка: соединение с БД (пригодится для коннектора)."""

    def _load(self) -> list[dict[str, Any]]:
        """Загрузить данные из файла."""
        try:
            with self._filepath.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, data: list[dict[str, Any]]) -> None:
        """Сохранить данные в файл."""
        with self._filepath.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load()
        entry = aeroplane.to_dict()
        # защита от дублей по позывному
        for item in data:
            if item.get("callsign") == entry["callsign"]:
                return
        data.append(entry)
        self._save(data)

    def get_aeroplanes(self, **criteria: Any) -> list[Aeroplane]:
        result = Aeroplane.cast_to_object_list(self._load())
        country = criteria.get("country")
        if country:
            needle = country.lower()
            result = [
                p for p in result if needle in p.origin_country.lower()
            ]
        min_alt = criteria.get("min_alt")
        max_alt = criteria.get("max_alt")
        if min_alt is not None:
            result = [p for p in result if p.baro_altitude >= min_alt]
        if max_alt is not None:
            result = [p for p in result if p.baro_altitude <= max_alt]
        return result

    def delete_aeroplane(
        self, aeroplane: Union[Aeroplane, str]
    ) -> bool:
        callsign = (
            aeroplane if isinstance(aeroplane, str) else aeroplane.callsign
        )
        data = self._load()
        new_data = [
            item for item in data if item.get("callsign") != callsign
        ]
        if len(new_data) < len(data):
            self._save(new_data)
            return True
        return False
