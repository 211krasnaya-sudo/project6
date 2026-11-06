import pytest

from src.aeroplane import Aeroplane
from src.utils import (filter_aeroplanes, get_aeroplanes_by_altitude,
                       get_top_aeroplanes, sort_aeroplanes)


def make_plane(callsign: str, altitude: float) -> Aeroplane:
    return Aeroplane(callsign, "Spain",
                     200, altitude)


def test_filter_by_countries():
    planes = [
        make_plane("A", 1000),
        Aeroplane("B", "France",
                  150, 2000),
    ]
    assert len(filter_aeroplanes(planes, ["spain"])) == 1
    assert len(filter_aeroplanes(planes, [])) == 2


def test_sort_desc_and_top_n():
    planes = [make_plane("A", 1000),
              make_plane("B", 5000),
              make_plane("C", 3000)]
    sorted_planes = sort_aeroplanes(planes)
    assert [p.callsign for p in sorted_planes] == ["B", "C", "A"]
    top = get_top_aeroplanes(sorted_planes, 2)
    assert [p.callsign for p in top] == ["B", "C"]


def test_get_by_altitude_ok():
    planes = [make_plane("A", 100),
              make_plane("B", 500)]
    result = get_aeroplanes_by_altitude(planes,
                                        "100-500")
    assert len(result) == 2


def test_get_by_altitude_invalid_range():
    planes = [make_plane("A", 100)]
    with pytest.raises(ValueError):
        get_aeroplanes_by_altitude(planes, "abc")
    with pytest.raises(ValueError):
        get_aeroplanes_by_altitude(planes, "500-100")
