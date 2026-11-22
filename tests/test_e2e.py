# tests/test_e2e.py
import json
import os
import subprocess
import sys

import pytest

from wallet import main


def test_online_report_with_a_fake_api(tmp_path, monkeypatch, capsys, fake_api):
    monkeypatch.setenv('WALLET_FILE', str(tmp_path / 'expenses.json'))
    monkeypatch.delenv('WALLET_OFFLINE', raising=False)
    main(['add', '12.50', 'EUR', 'food', 'Pizza'])
    main(['add', '22', 'USD', 'transport', 'Taxi'])
    capsys.readouterr()
    assert main(['report']) == 0
    assert capsys.readouterr().out.splitlines()[-1] == 'total        32.50 EUR'
    assert fake_api.call_count == 1


def test_unknown_currency_from_the_api(tmp_path, monkeypatch, capsys, fake_api):
    monkeypatch.setenv('WALLET_FILE', str(tmp_path / 'expenses.json'))
    monkeypatch.delenv('WALLET_OFFLINE', raising=False)
    monkeypatch.setattr('wallet.KNOWN', ['EUR', 'UAH'])
    main(['add', '100', 'UAH', 'food', 'Borscht'])
    assert main(['report']) == 1
    assert capsys.readouterr().err == 'error: unknown currency: UAH\n'


def run_wallet(words, data_file):
    env = {**os.environ, 'WALLET_OFFLINE': '1', 'WALLET_FILE': str(data_file)}
    return subprocess.run([sys.executable, 'wallet.py'] + words,
                          env=env, capture_output=True, text=True)


@pytest.mark.slow
def test_real_process_add_and_report(tmp_path):
    data_file = tmp_path / 'expenses.json'
    added = run_wallet(['add', '12.50', 'EUR', 'food', 'Pizza'], data_file)
    assert added.returncode == 0
    assert added.stdout == 'Added: 12.50 EUR, food, Pizza\n'
    report = run_wallet(['report'], data_file)
    assert report.returncode == 0
    assert report.stdout.splitlines()[-1] == 'total        12.50 EUR'
    assert json.loads(data_file.read_text())[0]['note'] == 'Pizza'


@pytest.mark.slow
def test_real_process_bad_amount(tmp_path):
    result = run_wallet(['add', 'abc', 'EUR', 'food', 'Pizza'], tmp_path / 'e.json')
    assert result.returncode == 1
    assert result.stdout == ''
    assert result.stderr == 'error: not a number: abc\n'
