import pytest

from src.aeroplane import Aeroplane


def test_create_valid_aeroplane():
    plane = Aeroplane("UAL1621", "United States",
                      268.79, 10203.18)
    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 268.79
    assert plane.baro_altitude == 10203.18


@pytest.mark.parametrize("callsign,velocity,altitude", [
    ("", "US", 100),            # пустой позывной
    ("X", "", 100),             # пустая страна
    ("X", "US", -5),            # отрицательная высота
    ("X", "US", "abc"),         # нечисловая высота
])
def test_validation_errors(callsign, velocity, altitude):
    with pytest.raises(ValueError):
        Aeroplane(callsign, velocity, 100, altitude)


def test_compare_by_altitude():
    low = Aeroplane("LOW1", "US", 100,
                    1000)
    high = Aeroplane("HIGH1", "US", 100,
                     10000)
    assert low < high
    assert high > low
    assert (low == high) is False


def test_compare_by_velocity():
    slow = Aeroplane("SLOW", "US", 50,
                     1000)
    fast = Aeroplane("FAST", "US", 300,
                     1000)
    assert slow.compare_by_velocity(fast) == -1
    assert fast.compare_by_velocity(slow) == 1
    assert slow.compare_by_velocity(slow) == 0


def test_compare_with_not_aeroplane():
    plane = Aeroplane("X", "US", 100,
                      1000)
    with pytest.raises(TypeError):
        plane.compare_by_velocity("not a plane")


def test_cast_to_object_list_skips_invalid():
    raw = [
        {"callsign": "AAA", "origin_country": "Spain",
         "velocity": 200, "baro_altitude": 5000},
        {"callsign": "", "origin_country": "Spain",
         "velocity": 200, "baro_altitude": 5000},
        {"callsign": "BBB", "origin_country": "France",
         "velocity": 150, "baro_altitude": 3000},
    ]
    result = Aeroplane.cast_to_object_list(raw)
    assert len(result) == 2
    assert result[0].callsign == "AAA"


def test_str_is_readable():
    plane = Aeroplane("UAL1621", "United States",
                      268.79, 10203.18)
    text = str(plane)
    assert "UAL1621" in text
    assert "United States" in text
