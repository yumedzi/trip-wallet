# Trip Wallet

A small command-line expense tracker for a trip: it records expenses in several currencies, stores them in a JSON file, converts them with a real exchange-rate API and prints a report. It is the course project of [Zero to Hero](https://book.onpy.dev/), built in the Level Up part and tested in the Testing part.

## This branch: session 4, Working with Real Data

JsonStorage, rates.py (FixedRates, FrankfurterRates over a real web API) and wallet.py, the command-line program. From here on the program itself does not change.

Chapter: [Working with Real Data](https://book.onpy.dev/chapter/zero11-real-data/)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python wallet.py add 12.50 EUR food Pizza
python wallet.py report
WALLET_OFFLINE=1 python wallet.py report
```

## All sessions

Each branch holds the project as it stands at the end of one chapter; `main` is the finished project.

- [Functions Level Up](https://book.onpy.dev/chapter/zero08-functions-level-up/) → `session-1-functions-level-up`
- [Errors and Decorators](https://book.onpy.dev/chapter/zero09-errors-decorators/) → `session-2-errors-and-decorators`
- [Objects for Testing](https://book.onpy.dev/chapter/zero10-objects-testing/) → `session-3-objects-for-testing`
- [Working with Real Data](https://book.onpy.dev/chapter/zero11-real-data/) → `session-4-real-data`
- [Pytest Basics](https://book.onpy.dev/chapter/zero12-pytest-basics/) → `session-5-pytest-basics`
- [Fixtures](https://book.onpy.dev/chapter/zero13-fixtures/) → `session-6-fixtures`
- [Mocking](https://book.onpy.dev/chapter/zero14-mocking/) → `session-7-mocking`
- [Project Structure](https://book.onpy.dev/chapter/zero15-project-structure/) → `session-8-project-structure`
