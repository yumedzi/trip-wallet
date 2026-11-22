import pytest

from money import make_expense
from storage import Storage, MemoryStorage


def test_new_memory_storage_is_empty():
    assert MemoryStorage().load() == []


def test_add_then_load():
    storage = MemoryStorage()
    storage.add(make_expense(amount=5))
    assert storage.load() == [make_expense(amount=5)]
    assert storage.count() == 1


def test_load_returns_a_copy():
    storage = MemoryStorage()
    storage.add(make_expense(amount=5))
    storage.load().clear()
    assert storage.count() == 1


def test_base_storage_cannot_load():
    with pytest.raises(NotImplementedError):
        Storage().load()
