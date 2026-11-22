import pytest

from errors import UnknownCurrencyError
from rates import FrankfurterRates

pytestmark = pytest.mark.network


def test_usd_rate_is_a_sensible_number():
    rate = FrankfurterRates().rate('USD')
    assert 0.5 < rate < 2


def test_hryvnia_is_unknown_to_the_service():
    with pytest.raises(UnknownCurrencyError):
        FrankfurterRates().rate('UAH')
