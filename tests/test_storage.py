import json

import pytest

from money import make_expense
from storage import Storage, MemoryStorage, JsonStorage


def test_new_memory_storage_is_empty():
    assert MemoryStorage().load() == []


def test_add_then_load():
    storage = MemoryStorage()
    storage.add(make_expense(amount=5))
    assert storage.load() == [make_expense(amount=5)]
    assert storage.count() == 1


def test_load_returns_a_copy(storage):
    storage.load().clear()
    assert storage.count() == 3


def test_base_storage_cannot_load():
    with pytest.raises(NotImplementedError):
        Storage().load()


def test_missing_json_file_loads_empty(json_storage):
    assert json_storage.load() == []


def test_json_save_then_load(json_storage, expenses):
    json_storage.save(expenses)
    assert json_storage.load() == expenses


def test_json_add_keeps_older_expenses(json_storage, expenses):
    json_storage.save(expenses)
    json_storage.add(make_expense(amount=99, note='Hotel'))
    assert json_storage.count() == 4


def test_json_file_holds_a_list_of_dicts(json_storage, expenses):
    json_storage.save(expenses)
    data = json.loads(json_storage.path.read_text())
    assert data[0] == {'amount': 12.5, 'currency': 'EUR',
                       'category': 'food', 'note': 'Pizza'}


def test_json_creates_missing_folders(tmp_path):
    path = tmp_path / 'data' / 'trip' / 'expenses.json'
    JsonStorage(path).save([make_expense(amount=5)])
    assert path.exists()


def test_broken_json_file_raises(json_storage):
    json_storage.path.write_text('not json')
    with pytest.raises(json.JSONDecodeError):
        json_storage.load()
