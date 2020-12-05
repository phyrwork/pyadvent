import pytest

from .boarding import Seat, parse


@pytest.mark.parametrize(['code', 'seat'], [
    pytest.param('FBFBBFFRLR', (44, 5)),
])
def test_parse(code: str, seat: Seat):
    assert parse(code) == seat
