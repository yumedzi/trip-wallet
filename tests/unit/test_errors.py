import pytest

from errors import (WalletError, InvalidAmountError, UnknownCurrencyError,
                    parse_amount, check_currency)


@pytest.mark.parametrize('text, expected', [
    ('12', 12.0),
    ('12,50', 12.5),
    (' 7 ', 7.0),
    ('0.01', 0.01),
], ids=['whole', 'comma', 'spaces', 'cent'])
def test_parse_amount_good(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize('text', ['', 'abc', '-3', '0'])
def test_parse_amount_bad(text):
    with pytest.raises(InvalidAmountError):
        parse_amount(text)


def test_parse_amount_explains_negative():
    with pytest.raises(InvalidAmountError, match='must be positive'):
        parse_amount('-3')


def test_check_currency_upper_cases():
    assert check_currency(' usd ', ['EUR', 'USD']) == 'USD'


def test_unknown_currency_is_a_wallet_error():
    with pytest.raises(WalletError):
        check_currency('UAH', ['EUR', 'USD'])


def test_unknown_currency_names_the_code():
    with pytest.raises(UnknownCurrencyError, match='UAH'):
        check_currency('uah', ['EUR', 'USD'])
