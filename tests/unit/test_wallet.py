import pytest

from errors import UnknownCurrencyError
from money import make_expense
from storage import MemoryStorage
from wallet import Wallet


def test_report_has_one_line_per_category(wallet):
    assert wallet.report()[:2] == ['food         17.50 EUR',
                                   'transport    18.18 EUR']


def test_report_ends_with_the_total(wallet):
    assert wallet.report()[-1] == 'total        35.68 EUR'


def test_report_of_an_empty_wallet(fixed_rates):
    wallet = Wallet(MemoryStorage(), fixed_rates)
    assert wallet.report() == ['----------------------',
                               'total         0.00 EUR']


def test_add_goes_to_the_storage(wallet, storage):
    wallet.add(make_expense(amount=40, currency='GBP', category='hotel', note='Hotel'))
    assert storage.count() == 4


def test_report_with_an_unknown_currency_raises(wallet):
    wallet.add(make_expense(amount=1000, currency='JPY'))
    with pytest.raises(UnknownCurrencyError, match='JPY'):
        wallet.report()
