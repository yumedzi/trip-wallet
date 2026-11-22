import requests

from errors import UnknownCurrencyError, RatesUnavailableError

API_URL = 'https://api.frankfurter.dev/v1/latest'


class FixedRates:
    def __init__(self, table, base='EUR'):
        self.table = table
        self.base = base

    def rate(self, code):
        if code == self.base:
            return 1.0
        if code not in self.table:
            raise UnknownCurrencyError(f'unknown currency: {code}')
        return self.table[code]


class FrankfurterRates:
    def __init__(self, base='EUR'):
        self.base = base
        self.cache = {}

    def rate(self, code):
        if code == self.base:
            return 1.0
        if code not in self.cache:
            self.cache[code] = self.fetch(code)
        return self.cache[code]

    def fetch(self, code):
        params = {'base': self.base, 'symbols': code}
        try:
            response = requests.get(API_URL, params=params, timeout=5)
            if response.status_code == 404:
                raise UnknownCurrencyError(f'unknown currency: {code}')
            response.raise_for_status()
        except requests.RequestException as error:
            raise RatesUnavailableError(f'no rates for {code}: {error}')
        return response.json()['rates'][code]
