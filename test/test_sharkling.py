import pytest
from . import sharkling


@pytest.mark.skip(reason="Will currently run indefinitely")
def test_project():
    sharkling.Sharkling().run()
