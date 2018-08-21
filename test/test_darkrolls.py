import pytest
from . import darkrolls


@pytest.mark.parametrize('timestamp,roll_type', (
        ('201711111111', darkrolls.roll.Octs),
        ('201701111111', darkrolls.roll.Septs),
        ('201700111111', darkrolls.roll.Sexts),
        ('201700011111', darkrolls.roll.Quints),
        ('201700001111', darkrolls.roll.Quads),
        ('201700000111', darkrolls.roll.Trips),
        ('201700000011', darkrolls.roll.Dubs),
))
def test_check(timestamp, roll_type):
    assert darkrolls.roll.check(timestamp) == roll_type
