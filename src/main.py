"""Точка входа: взаимодействие с пользователем через консоль."""
from pathlib import Path

from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.storage import JSONSaver
from src.utils import (filter_aeroplanes, get_aeroplanes_by_altitude,
                       get_top_aeroplanes, print_aeroplanes, sort_aeroplanes)

DATA_FILE = Path("data/aircrafts.json")

MENU = """
Выберите действие:
1 - Топ N самолётов по высоте полёта
2 - Самолёты по стране регистрации
3 - Фильтр по диапазону высот
0 - Выход
"""


def user_interaction() -> None:
    api = AeroplanesAPI()
    saver = JSONSaver(DATA_FILE)

    country = input("Введите название страны: ").strip()
    if not country:
        print("Название страны не может быть пустым")
        return

    raw_aeroplanes = api.get_aeroplanes(country)
    if not raw_aeroplanes:
        print(f"Для страны '{country}' самолёты не найдены")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)
    for plane in aeroplanes:
        saver.add_aeroplane(plane)
    print(f"Найдено самолётов: {len(aeroplanes)}")

    while True:
        print(MENU)
        choice = input("Ваш выбор: ").strip()
        try:
            if choice == "1":
                n = int(input("Введите N: "))
                if n <= 0:
                    raise ValueError("N должно быть положительным числом")
                print_aeroplanes(
                    get_top_aeroplanes(sort_aeroplanes(aeroplanes), n)
                )
            elif choice == "2":
                words = input(
                    "Введите страны регистрации через пробел: "
                ).split()
                print_aeroplanes(filter_aeroplanes(aeroplanes, words))
            elif choice == "3":
                altitude_range = input(
                    "Введите диапазон высот (пример: 100-1500): "
                )
                print_aeroplanes(
                    get_aeroplanes_by_altitude(aeroplanes, altitude_range)
                )
            elif choice == "0":
                break
            else:
                print("Неизвестная команда, попробуйте снова")
        except ValueError as error:
            print(f"Ошибка ввода: {error}")


if __name__ == "__main__":
    user_interaction()
