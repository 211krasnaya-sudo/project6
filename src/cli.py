from typing import List
from .nominatim_api import NominatimAPI
from .opensky_api import OpenSkyAPI
from .models import Aeroplane
from .json_saver import JSONSaver

def get_bbox_for_country(country: str) -> tuple[float, float, float, float]:
    nominatim = NominatimAPI()
    bbox = nominatim.get_country_bbox(country)
    if not bbox:
        raise ValueError(f"Не удалось найти координаты для страны: {country}")
    return bbox["south"], bbox["north"], bbox["west"], bbox["east"]

def fetch_aircrafts(south: float, north: float, west: float, east: float) -> List[Aeroplane]:
    opensky = OpenSkyAPI()
    raw_planes = opensky.get_aircrafts_in_bbox(south, north, west, east)
    return Aeroplane.cast_to_object_list(raw_planes)

def filter_by_altitude(planes: List[Aeroplane], min_alt: float, max_alt: float) -> List[Aeroplane]:
    return [p for p in planes if min_alt <= p.baro_altitude <= max_alt]

def sort_by_altitude_desc(planes: List[Aeroplane]) -> List[Aeroplane]:
    return sorted(planes, key=lambda p: p.baro_altitude, reverse=True)

def get_top_n(planes: List[Aeroplane], n: int) -> List[Aeroplane]:
    return planes[:n]

def user_interaction():
    country = input("Введите название страны для запроса самолётов: ").strip()
    try:
        south, north, west, east = get_bbox_for_country(country)
        print(f"Координаты страны: south={south}, north={north}, west={west}, east={east}")
    except Exception as e:
        print(f"Ошибка получения координат: {e}")
        return

    planes = fetch_aircrafts(south, north, west, east)
    print(f"Найдено самолётов: {len(planes)}")

    top_n_str = input("Сколько самолётов показать в топе по высоте (N)? ").strip()
    top_n = int(top_n_str) if top_n_str.isdigit() else 10

    min_alt_str, max_alt_str = input("Диапазон высот (мин макс, в метрах, через пробел): ").strip().split()
    min_alt, max_alt = float(min_alt_str), float(max_alt_str)

    filtered = filter_by_altitude(planes, min_alt, max_alt)
    sorted_planes = sort_by_altitude_desc(filtered)
    top_planes = get_top_n(sorted_planes, top_n)

    print("\nТоп самолётов по высоте:")
    for p in top_