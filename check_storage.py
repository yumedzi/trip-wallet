from dataclasses import asdict

from money import Expense, make_expense, total, by_category
from storage import Storage, MemoryStorage

store = MemoryStorage()
trip = [
    make_expense(amount=12.5, category='food', note='Pizza'),
    make_expense(amount=8, category='transport', note='Taxi'),
    make_expense(amount=5, category='food', note='Coffee'),
]
for expense in trip:
    store.add(expense)

assert store.count() == 3
assert store.load() == trip
assert total(store.load(), 'food') == 17.5
assert by_category(store.load()) == {'food': 17.5, 'transport': 8}
assert isinstance(store, Storage)
assert asdict(trip[1])['note'] == 'Taxi'
print(store.load()[0])
print('check_storage.py: all checks passed')
