# tests/test_rates.py
import pytest
import requests

import rates
from errors import RatesUnavailableError, UnknownCurrencyError
from rates import FrankfurterRates


def test_fixed_rate(fixed_rates):
    assert fixed_rates.rate('GBP') == 0.88


def test_fixed_rates_unknown_currency(fixed_rates):
    with pytest.raises(UnknownCurrencyError, match='JPY'):
        fixed_rates.rate('JPY')


def test_frankfurter_rate(fake_api):
    assert FrankfurterRates().rate('USD') == 1.1


def test_home_currency_needs_no_request(fake_api):
    assert FrankfurterRates().rate('EUR') == 1.0
    assert fake_api.call_count == 0


def test_asks_once_with_a_timeout(fake_api):
    usd_rates = FrankfurterRates()
    usd_rates.rate('USD')
    usd_rates.rate('USD')
    fake_api.assert_called_once_with(rates.API_URL,
                                     params={'base': 'EUR', 'symbols': 'USD'},
                                     timeout=5)


def test_404_means_unknown_currency(fake_api):
    with pytest.raises(UnknownCurrencyError, match='UAH'):
        FrankfurterRates().rate('UAH')


def test_no_network_means_rates_unavailable(fake_api):
    fake_api.side_effect = requests.ConnectionError('no network')
    with pytest.raises(RatesUnavailableError, match='USD'):
        FrankfurterRates().rate('USD')
