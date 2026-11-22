import pytest

from money import Expense, make_expense, total, by_category, sample_expenses


def test_make_expense_fills_defaults():
    expense = make_expense(amount=5)
    assert expense == Expense(5, 'EUR', 'other', '')


def test_make_expense_keeps_given_fields():
    expense = make_expense(amount=12.5, category='food', note='Pizza')
    assert expense.category == 'food'
    assert expense.note == 'Pizza'


def test_total_of_empty_list_is_zero():
    assert total([]) == 0


def test_total_adds_all_amounts():
    expenses = [make_expense(amount=12.5), make_expense(amount=20)]
    assert total(expenses) == 32.5


def test_total_of_one_category():
    expenses = [make_expense(amount=12.5, category='food'),
                make_expense(amount=20, category='transport')]
    assert total(expenses, 'food') == 12.5


def test_total_of_small_prices():
    expenses = [make_expense(amount=0.1), make_expense(amount=0.2)]
    assert total(expenses) == pytest.approx(0.3)


def test_by_category_groups_amounts():
    expenses = sample_expenses(2, category='food') + [make_expense(amount=5)]
    assert by_category(expenses) == {'food': 30, 'other': 5}


def test_sample_expenses_count_and_overrides():
    expenses = sample_expenses(3, currency='USD')
    assert len(expenses) == 3
    assert {e.currency for e in expenses} == {'USD'}
