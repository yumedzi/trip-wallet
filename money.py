from dataclasses import dataclass, asdict


@dataclass
class Expense:
    amount: float
    currency: str = 'EUR'
    category: str = 'other'
    note: str = ''


DEFAULTS = asdict(Expense(0))


def make_expense(**fields):
    return Expense(**{**DEFAULTS, **fields})


def total(expenses, category=None):
    if category is None:
        return sum([e.amount for e in expenses])
    return sum([e.amount for e in expenses if e.category == category])


def by_category(expenses):
    categories = sorted({e.category for e in expenses})
    return {c: total(expenses, c) for c in categories}


def sample_expenses(count=3, **overrides):
    return [make_expense(**{'amount': 10 * n, 'note': f'Item {n}', **overrides})
            for n in range(1, count + 1)]
