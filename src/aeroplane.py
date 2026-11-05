"""Класс самолёта: инкапсуляция, валидация, сравнение."""
from typing import Any, Optional


class Aeroplane:
    """Самолёт с валидацией атрибутов и сравнением по высоте и скорости."""

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        baro_altitude: float,
        icao24: Optional[str] = None,
        on_ground: bool = False,
    ) -> None:
        if not isinstance(callsign, str) or not callsign.strip():
            raise ValueError("Позывной должен быть непустой строкой")
        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("Страна регистрации должна быть строкой")
        try:
            velocity = float(velocity)
            baro_altitude = float(baro_altitude)
        except (TypeError, ValueError):
            raise ValueError("Скорость и высота должны быть числами")
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        if baro_altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

        self._callsign = callsign.strip()
        self._origin_country = origin_country.strip()
        self._velocity = velocity
        self._baro_altitude = baro_altitude
        self._icao24 = icao24
        self._on_ground = bool(on_ground)

    # --- геттеры (инкапсуляция) ---
    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def velocity(self) -> float:
        return self._velocity

    @property
    def baro_altitude(self) -> float:
        return self._baro_altitude

    @property
    def icao24(self) -> Optional[str]:
        return self._icao24

    # --- сравнение по высоте ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._baro_altitude == other._baro_altitude

    def __lt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._baro_altitude < other._baro_altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._baro_altitude > other._baro_altitude

    # --- сравнение по скорости ---
    def compare_by_velocity(self, other: "Aeroplane") -> int:
        """1 — быстрее, -1 — медленнее, 0 — одинаковая скорость."""
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только самолёты")
        if self._velocity > other._velocity:
            return 1
        if self._velocity < other._velocity:
            return -1
        return 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "callsign": self._callsign,
            "origin_country": self._origin_country,
            "velocity": self._velocity,
            "baro_altitude": self._baro_altitude,
            "icao24": self._icao24,
            "on_ground": self._on_ground,
        }

    @classmethod
    def cast_to_object_list(
        cls, raw_list: list[dict[str, Any]]
    ) -> list["Aeroplane"]:
        """Преобразовать список словарей в объекты, пропуская битые."""
        result = []
        for entry in raw_list:
            try:
                result.append(cls(
                    callsign=entry.get("callsign") or "",
                    origin_country=entry.get("origin_country") or "",
                    velocity=entry.get("velocity") or 0.0,
                    baro_altitude=entry.get("baro_altitude") or 0.0,
                    icao24=entry.get("icao24"),
                    on_ground=bool(entry.get("on_ground")),
                ))
            except ValueError:
                continue
        return result

    def __str__(self) -> str:
        speed = self._velocity * 3.6
        return (
            f"Позывной: {self._callsign}, "
            f"страна: {self._origin_country}, "
            f"скорость: {speed:.1f} км/ч, "
            f"высота: {self._baro_altitude:.1f} м"
        )
