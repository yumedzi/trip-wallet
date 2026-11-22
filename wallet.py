import os
import sys

from errors import WalletError, parse_amount, check_currency
from money import make_expense
from rates import FixedRates, FrankfurterRates
from storage import JsonStorage

KNOWN = ['EUR', 'USD', 'GBP', 'PLN', 'CHF']
OFFLINE_RATES = {'USD': 1.1, 'GBP': 0.88, 'PLN': 4.25, 'CHF': 0.94}


def line(label, amount, currency):
    return f'{label:<12}{amount:>6.2f} {currency}'


class Wallet:
    def __init__(self, storage, rates, home='EUR'):
        self.storage = storage
        self.rates = rates
        self.home = home

    def add(self, expense):
        self.storage.add(expense)

    def in_home(self, expense):
        return expense.amount / self.rates.rate(expense.currency)

    def report(self):
        totals = {}
        for expense in self.storage.load():
            old = totals.get(expense.category, 0)
            totals[expense.category] = old + self.in_home(expense)
        lines = [line(c, totals[c], self.home) for c in sorted(totals)]
        lines.append('-' * 22)
        lines.append(line('total', sum(totals.values()), self.home))
        return lines


def add_command(wallet, args):
    if len(args) != 4:
        raise WalletError('usage: add AMOUNT CURRENCY CATEGORY NOTE')
    amount = parse_amount(args[0])
    currency = check_currency(args[1], KNOWN)
    category, note = args[2], args[3]
    wallet.add(make_expense(amount=amount, currency=currency,
                            category=category, note=note))
    print(f'Added: {amount:.2f} {currency}, {category}, {note}')


def report_command(wallet, args):
    for text in wallet.report():
        print(text)


COMMANDS = {'add': add_command, 'report': report_command}


def make_wallet():
    storage = JsonStorage(os.environ.get('WALLET_FILE', 'data/expenses.json'))
    if os.environ.get('WALLET_OFFLINE') == '1':
        rates = FixedRates(OFFLINE_RATES)
    else:
        rates = FrankfurterRates()
    return Wallet(storage, rates)


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print('usage: python wallet.py add|report ...', file=sys.stderr)
        return 2
    try:
        COMMANDS[argv[0]](make_wallet(), argv[1:])
    except WalletError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
