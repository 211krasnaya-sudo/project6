import pytest

from src.api import AeroplanesAPI

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OPENSKY_URL = "https://opensky-network.org/api/states/all"

NOMINATIM_RESPONSE = [{"boundingbox": ["36.0", "43.9", "-9.3", "4.3"]}]
OPENSKY_RESPONSE = {"time": 0, "states": [
    ["abc123", "UAL1621 ", "United States", None, None,
     1.0, 2.0, 10203.18, False, 268.79, 90, 0, None,
     10000, "1200", False, 0],
]}


@pytest.fixture
def api() -> AeroplanesAPI:
    return AeroplanesAPI()


def test_get_coordinates_ok(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=NOMINATIM_RESPONSE)
    coords = api.get_coordinates("Spain")
    assert coords == {
        "south": 36.0, "north": 43.9, "west": -9.3, "east": 4.3
    }


def test_get_coordinates_not_found(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=[])
    assert api.get_coordinates("Nowhere") is None


def test_get_coordinates_http_error(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, status_code=500)
    assert api.get_coordinates("Spain") is None


def test_get_coordinates_bad_bbox(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=[{"boundingbox": [1, 2]}])
    assert api.get_coordinates("Spain") is None


def test_get_aeroplanes_ok(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=NOMINATIM_RESPONSE)
    requests_mock.get(OPENSKY_URL, json=OPENSKY_RESPONSE)
    planes = api.get_aeroplanes("Spain")
    assert len(planes) == 1
    assert planes[0]["callsign"] == "UAL1621"
    assert planes[0]["velocity"] == 268.79


def test_get_aeroplanes_country_not_found(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=[])
    assert api.get_aeroplanes("Nowhere") == []


def test_get_aeroplanes_http_error(requests_mock, api):
    requests_mock.get(NOMINATIM_URL, json=NOMINATIM_RESPONSE)
    requests_mock.get(OPENSKY_URL, status_code=429)
    assert api.get_aeroplanes("Spain") == []
