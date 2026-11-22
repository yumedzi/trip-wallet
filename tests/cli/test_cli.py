from storage import JsonStorage
from wallet import main


def test_add_prints_a_confirmation(cli_env, capsys):
    assert main(['add', '12,50', 'eur', 'food', 'Pizza']) == 0
    assert capsys.readouterr().out == 'Added: 12.50 EUR, food, Pizza\n'


def test_add_saves_to_the_file(cli_env):
    main(['add', '20', 'USD', 'transport', 'Taxi'])
    saved = JsonStorage(cli_env).load()
    assert [e.note for e in saved] == ['Taxi']


def test_report_after_two_adds(cli_env, capsys):
    main(['add', '12.50', 'EUR', 'food', 'Pizza'])
    main(['add', '22', 'USD', 'transport', 'Taxi'])
    capsys.readouterr()
    assert main(['report']) == 0
    assert capsys.readouterr().out == ('food         12.50 EUR\n'
                                       'transport    20.00 EUR\n'
                                       '----------------------\n'
                                       'total        32.50 EUR\n')


def test_bad_amount_is_exit_code_1(cli_env, capsys):
    assert main(['add', 'abc', 'EUR', 'food', 'Pizza']) == 1
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == 'error: not a number: abc\n'


def test_unknown_command_is_exit_code_2(cli_env, capsys):
    assert main(['delete']) == 2
    assert 'usage' in capsys.readouterr().err


def test_add_needs_four_words(cli_env, capsys):
    assert main(['add', '12.50', 'EUR']) == 1
    assert capsys.readouterr().err == 'error: usage: add AMOUNT CURRENCY CATEGORY NOTE\n'
