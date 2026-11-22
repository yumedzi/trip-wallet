import json
from dataclasses import asdict
from pathlib import Path

from money import Expense


class Storage:
    def load(self):
        raise NotImplementedError('a child class must write load()')

    def save(self, expenses):
        raise NotImplementedError('a child class must write save()')

    def add(self, expense):
        expenses = self.load()
        expenses.append(expense)
        self.save(expenses)

    def count(self):
        return len(self.load())


class MemoryStorage(Storage):
    def __init__(self):
        super().__init__()
        self.expenses = []

    def load(self):
        return list(self.expenses)

    def save(self, expenses):
        self.expenses = list(expenses)


class JsonStorage(Storage):
    def __init__(self, path):
        super().__init__()
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text())
        return [Expense(**item) for item in data]

    def save(self, expenses):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(e) for e in expenses]
        self.path.write_text(json.dumps(data, indent=2))
