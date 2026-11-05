from src.utils import print_aeroplanes

from src.aeroplane import Aeroplane


def test_print_empty(capsys):
    print_aeroplanes([])
    assert "не найдено" in capsys.readouterr().out


def test_print_planes(capsys):
    plane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    print_aeroplanes([plane])
    output = capsys.readouterr().out
    assert "UAL1621" in output
    assert "1." in output
