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
