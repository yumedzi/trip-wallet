class WalletError(Exception):
    pass

class InvalidAmountError(WalletError):
    pass

class UnknownCurrencyError(WalletError):
    pass

class RatesUnavailableError(WalletError):
    pass


def parse_amount(text):
    cleaned = text.strip().replace(',', '.')
    if cleaned == '':
        raise InvalidAmountError('amount is empty')
    try:
        amount = float(cleaned)
    except ValueError:
        raise InvalidAmountError(f'not a number: {text}')
    if amount <= 0:
        raise InvalidAmountError(f'amount must be positive, got {text}')
    return amount


def check_currency(code, known):
    code = code.strip().upper()
    if code not in known:
        raise UnknownCurrencyError(f'unknown currency: {code}')
    return code
