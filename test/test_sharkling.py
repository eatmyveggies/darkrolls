import pytest
from . import sharkling


@pytest.mark.skip(reason="Will currently run indefinitely, just a sanity test")
def test_project():
    sharkling.Sharkling().run()


@pytest.mark.parametrize('timestamp,roll_type', (
        ('201711111111', sharkling.roll.Octs),
        ('201701111111', sharkling.roll.Septs),
        ('201700111111', sharkling.roll.Sexts),
        ('201700011111', sharkling.roll.Quints),
        ('201700001111', sharkling.roll.Quads),
        ('201700000111', sharkling.roll.Trips),
        ('201700000011', sharkling.roll.Dubs),
))
def test_check(timestamp, roll_type):
    assert sharkling.roll.check(timestamp) == roll_type
