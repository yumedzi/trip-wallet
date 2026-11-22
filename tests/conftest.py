import pytest

from money import make_expense
from rates import FixedRates
from storage import MemoryStorage, JsonStorage
from wallet import Wallet


@pytest.fixture
def expenses():
    """Pizza and Coffee in EUR, a Taxi in USD."""
    return [make_expense(amount=12.5, category='food', note='Pizza'),
            make_expense(amount=20, currency='USD', category='transport', note='Taxi'),
            make_expense(amount=5, category='food', note='Coffee')]


@pytest.fixture
def storage(expenses):
    """A MemoryStorage that already holds the three expenses."""
    storage = MemoryStorage()
    storage.save(expenses)
    return storage


@pytest.fixture
def json_storage(tmp_path):
    """An empty JsonStorage with its file in a fresh temporary folder."""
    return JsonStorage(tmp_path / 'expenses.json')


@pytest.fixture
def fixed_rates():
    """Offline rates: 1 EUR = 1.1 USD = 0.88 GBP."""
    return FixedRates({'USD': 1.1, 'GBP': 0.88})


@pytest.fixture
def wallet(storage, fixed_rates):
    """A Wallet over the storage fixture with fixed rates."""
    return Wallet(storage, fixed_rates)


@pytest.fixture
def cli_env(tmp_path, monkeypatch):
    """main() runs offline with its data file in tmp_path; returns that path."""
    path = tmp_path / 'expenses.json'
    monkeypatch.setenv('WALLET_FILE', str(path))
    monkeypatch.setenv('WALLET_OFFLINE', '1')
    return path
