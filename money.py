DEFAULTS = {'amount': 0, 'currency': 'EUR', 'category': 'other', 'note': ''}


def make_expense(**fields):
    return {**DEFAULTS, **fields}


def add_all(*amounts):
    result = 0
    for amount in amounts:
        result = result + amount
    return result


def total(expenses, category=None):
    if category is None:
        return sum([e['amount'] for e in expenses])
    return sum([e['amount'] for e in expenses if e['category'] == category])


def by_category(expenses):
    categories = sorted({e['category'] for e in expenses})
    return {c: total(expenses, c) for c in categories}


def sample_expenses(count=3, **overrides):
    return [make_expense(**{'amount': 10 * n, 'note': f'Item {n}', **overrides})
            for n in range(1, count + 1)]


if __name__ == '__main__':
    trip = [
        make_expense(amount=12.5, category='food', note='Pizza'),
        make_expense(amount=8, category='transport', note='Taxi'),
        make_expense(amount=5, category='food', note='Coffee'),
    ]
    assert add_all(1, 2, 3) == 6
    assert total(trip) == 25.5
    assert total(trip, 'food') == 17.5
    assert by_category(trip) == {'food': 17.5, 'transport': 8}
    assert len(sample_expenses(2, category='food')) == 2
    assert sample_expenses(1)[0]['currency'] == 'EUR'
    for category, amount in by_category(trip).items():
        print(category, amount)
    print('money.py: all checks passed')
