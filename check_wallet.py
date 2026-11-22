from errors import InvalidAmountError, WalletError, UnknownCurrencyError, parse_amount, check_currency
from decorators import log_call, timed
import money


def raises(error_type, func, *args):
    try:
        func(*args)
    except error_type:
        return True
    return False


assert parse_amount('12,50') == 12.5
for bad in ['', 'abc', '-3', '0']:
    assert raises(InvalidAmountError, parse_amount, bad), bad
assert raises(WalletError, parse_amount, 'abc')
assert raises(UnknownCurrencyError, check_currency, 'UAH', ['EUR', 'USD'])

add_all = log_call(money.add_all)
total = timed(money.total)
trip = [money.make_expense(amount=12.5), money.make_expense(amount=8)]
assert add_all(12.5, 8) == 20.5
assert total(trip) == 20.5
print('check_wallet.py: all checks passed')
