"""Функции фильтрации, сортировки и вывода самолётов."""
from typing import List

from src.aeroplane import Aeroplane


def filter_aeroplanes(
    aeroplanes: List[Aeroplane], countries: List[str]
) -> List[Aeroplane]:
    """Фильтр по странам регистрации (регистронезависимо)."""
    if not countries:
        return aeroplanes
    needles = [c.lower() for c in countries]
    return [
        p for p in aeroplanes
        if p.origin_country.lower() in needles
    ]


def get_aeroplanes_by_altitude(
    aeroplanes: List[Aeroplane], altitude_range: str
) -> List[Aeroplane]:
    """Фильтр по диапазону высот. Пример строки: '100-1500'."""
    try:
        parts = [p.strip() for p in altitude_range.split("-")]
        min_alt, max_alt = float(parts[0]), float(parts[1])
    except (ValueError, IndexError):
        raise ValueError("Диапазон высот задан неверно. Пример: 100-1500")
    if min_alt > max_alt:
        raise ValueError("Минимум высоты больше максимума")
    return [p for p in aeroplanes if min_alt <= p.baro_altitude <= max_alt]


def sort_aeroplanes(aeroplanes: List[Aeroplane]) -> List[Aeroplane]:
    """Сортировка по высоте: DESC."""
    return sorted(aeroplanes, key=lambda p: p.baro_altitude, reverse=True)


def get_top_aeroplanes(
    aeroplanes: List[Aeroplane], top_n: int
) -> List[Aeroplane]:
    """Топ N самолётов."""
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """Человекочитаемый вывод списка самолётов."""
    if not aeroplanes:
        print("Самолётов не найдено")
        return
    for index, plane in enumerate(aeroplanes, start=1):
        print(f"{index}. {plane}")
