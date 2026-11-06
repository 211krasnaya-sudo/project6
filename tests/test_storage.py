from pathlib import Path

import pytest

from src.aeroplane import Aeroplane
from src.storage import JSONSaver


@pytest.fixture
def saver(tmp_path: Path) -> JSONSaver:
    return JSONSaver(filepath=tmp_path / "aircrafts.json")


def make_plane(callsign: str, altitude: float = 5000)\
        -> Aeroplane:
    return Aeroplane(callsign, "Spain",
                     200, altitude)


def test_add_and_get(saver: JSONSaver):
    plane = make_plane("AAA", 3000)
    saver.add_aeroplane(plane)
    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].callsign == "AAA"


def test_add_duplicate_ignored(saver: JSONSaver):
    saver.add_aeroplane(make_plane("AAA"))
    saver.add_aeroplane(make_plane("AAA"))
    assert len(saver.get_aeroplanes()) == 1


def test_get_by_country(saver: JSONSaver):
    saver.add_aeroplane(make_plane("AAA"))
    saver.add_aeroplane(Aeroplane("BBB", "France",
                                  150, 3000))
    assert len(saver.get_aeroplanes(country="spain")) == 1
    assert len(saver.get_aeroplanes(country="France")) == 1


def test_get_by_altitude_criteria(saver: JSONSaver):
    saver.add_aeroplane(make_plane("LOW", 1000))
    saver.add_aeroplane(make_plane("HIGH", 9000))
    assert len(saver.get_aeroplanes(min_alt=5000)) == 1
    assert len(saver.get_aeroplanes(max_alt=5000)) == 1


def test_delete_by_callsign(saver: JSONSaver):
    saver.add_aeroplane(make_plane("AAA"))
    assert saver.delete_aeroplane("AAA") is True
    assert saver.get_aeroplanes() == []
    assert saver.delete_aeroplane("AAA") is False


def test_delete_by_object(saver: JSONSaver):
    plane = make_plane("AAA")
    saver.add_aeroplane(plane)
    assert saver.delete_aeroplane(plane) is True


def test_corrupted_file_returns_empty(tmp_path: Path):
    filepath = tmp_path / "broken.json"
    filepath.write_text("not json", encoding="utf-8")
    saver = JSONSaver(filepath=filepath)
    assert saver.get_aeroplanes() == []
