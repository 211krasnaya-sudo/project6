"""Тесты функции user_interaction."""
import pytest

import src.main
from src.main import user_interaction

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPENSKY_URL = "https://opensky-network.org/api/states/all"

STATES = [
    ["abc123", "AAA ", "Spain", None, None,
     1.0, 2.0, 5000.0, False, 200.0, 90, 0, None,
     4000.0, "1000", False, 0],
    ["def456", "BBB ", "France", None, None,
     2.0, 3.0, 9000.0, False, 250.0, 180, 0, None,
     8000.0, "2000", False, 0],
]


@pytest.fixture(autouse=True)
def temp_data_file(monkeypatch, tmp_path):
    """Перенаправляем JSON-файл проекта во временную папку."""
    fake = tmp_path / "aircrafts.json"
    monkeypatch.setattr("src.main.DATA_FILE", fake)


@pytest.fixture
def mocked_api(requests_mock):
    requests_mock.get(
        NOMINATIM_URL,
        json=[{"boundingbox": ["36.0", "43.9", "-9.3", "4.3"]}],
    )
    requests_mock.get(
        OPENSKY_URL, json={"time": 0, "states": STATES}
    )


def feed(monkeypatch, answers):
    iterator = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *args: next(iterator))


def test_empty_country_exits(monkeypatch, capsys):
    feed(monkeypatch, ["   "])
    user_interaction()
    assert "не может быть пустым" in capsys.readouterr().out


def test_country_not_found(monkeypatch, requests_mock, capsys):
    requests_mock.get(NOMINATIM_URL, json=[])
    feed(monkeypatch, ["Atlantida"])
    user_interaction()
    assert "не найдены" in capsys.readouterr().out


def test_top_n_flow(mocked_api, monkeypatch, capsys):
    """Выбор 1: топ N по высоте, затем выход."""
    feed(monkeypatch, ["Spain", "1", "2", "0"])
    user_interaction()
    out = capsys.readouterr().out
    assert "Найдено самолётов: 2" in out
    # Топ DESC: сначала BBB (9000), потом AAA (5000)
    assert "BBB" in out
    assert "AAA" in out
    assert out.index("BBB") < out.index("AAA")


def test_top_n_invalid_value(mocked_api, monkeypatch, capsys):
    """Выбор 1 с нечисловым N -> ошибка ввода, затем выход."""
    feed(monkeypatch, ["Spain", "1", "abc", "0"])
    user_interaction()
    assert "Ошибка ввода" in capsys.readouterr().out


def test_top_n_negative(mocked_api, monkeypatch, capsys):
    feed(monkeypatch, ["Spain", "1", "-5", "0"])
    user_interaction()
    assert "Ошибка ввода" in capsys.readouterr().out


def test_filter_by_country(mocked_api, monkeypatch, capsys):
    """Выбор 2: фильтр по стране регистрации."""
    feed(monkeypatch, ["Spain", "2", "france", "0"])
    user_interaction()
    out = capsys.readouterr().out
    assert "BBB" in out
    assert "AAA" not in out


def test_filter_by_altitude(mocked_api, monkeypatch, capsys):
    """Выбор 3: фильтр по диапазону высот."""
    feed(monkeypatch, ["Spain", "3", "100-6000", "0"])
    user_interaction()
    out = capsys.readouterr().out
    assert "AAA" in out
    assert "BBB" not in out


def test_filter_altitude_invalid_range(mocked_api, monkeypatch,
                                       capsys):
    feed(monkeypatch, ["Spain", "3", "abc", "0"])
    user_interaction()
    assert "Ошибка ввода" in capsys.readouterr().out


def test_unknown_command(mocked_api, monkeypatch, capsys):
    feed(monkeypatch, ["Spain", "42", "0"])
    user_interaction()
    assert "Неизвестная команда" in capsys.readouterr().out


def test_planes_saved_to_file(mocked_api, monkeypatch, tmp_path):
    """После работы user_interaction самолёты сохраняются в JSON."""
    # запрос страны, затем выход из меню
    feed(monkeypatch, ["Spain", "0"])
    user_interaction()

    from src.storage import JSONSaver

    # читаем из модуля — увидим замоканный путь
    saver = JSONSaver(src.main.DATA_FILE)
    assert len(saver.get_aeroplanes()) == 2
