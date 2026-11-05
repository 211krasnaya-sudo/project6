from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Aeroplane:
    callsign: str
    origin_country: str
    velocity: float  # м/с
    baro_altitude: float  # метры

    # Дополнительные атрибуты по желанию
    icao24: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self):
        # Валидация
        if not self.callsign or not isinstance(self.callsign, str):
            raise ValueError("Callsign должен быть непустой строкой.")
        if self.velocity < 0:
            raise ValueError("Скорость не может быть отрицательной.")
        if self.baro_altitude < 0:
            raise ValueError("Высота не может быть отрицательной.")

    @classmethod
    def cast_to_object_list(cls, raw_list: list[dict]) -> list["Aeroplane"]:
        result = []
        for row in raw_list:
            try:
                obj = cls(
                    callsign=row.get("callsign", ""),
                    origin_country=row.get("origin_country", ""),
                    velocity=row.get("velocity", 0) or 0,
                    baro_altitude=row.get("baro_altitude", 0) or 0,
                    icao24=row.get("icao24"),
                    latitude=row.get("latitude"),
                    longitude=row.get("longitude"),
                )
                result.append(obj)
            except ValueError:
                # Пропускаем битые строки, чтобы не ломать весь список
                continue
        return result

    # Сравнение по высоте
    def __lt__(self, other: "Aeroplane") -> bool:
        return self.baro_altitude < other.baro_altitude

    def __le__(self, other: "Aeroplane") -> bool:
        return self.baro_altitude <= other.baro_altitude

    # Сравнение по скорости (если нужно отдельно)
    def compare_by_velocity(self, other: "Aeroplane") -> int:
        if self.velocity > other.velocity:
            return 1
        elif self.velocity < other.velocity:
            return -1
        return 0

    def __str__(self) -> str:
        alt_km = self.baro_altitude / 1000
        vel_kmh = self.velocity * 3.6
        return (
            f"Callsign: {self.callsign}, "
            f"Страна: {self.origin_country}, "
            f"Скорость: {vel_kmh:.1f} км/ч, "
            f"Высота: {alt_km:.2f} км"
        )
