# Personal Expense Tracker

A simple command-line expense tracker written in Python. It uses only the
standard library and stores data in a local SQLite database.

## Features
- Add expenses with amount, category, description and date
- List expenses, filtered by category and/or month
- Summary of spending by category, with percentage share
- Delete an expense by ID
- Export everything to CSV

## Requirements
Python 3.8 or newer. No third-party packages.

## Usage
```bash
python expense_tracker.py add 250 Food "Lunch with friends"
python expense_tracker.py add 1200 Transport "Train ticket" --date 2026-11-10
python expense_tracker.py list
python expense_tracker.py list --category Food --month 2026-11
python expense_tracker.py summary --month 2026-11
python expense_tracker.py delete 3
python expense_tracker.py export expenses.csv
```

## Run the tests
```bash
python -m unittest
```

## Ideas for next steps
- Monthly budgets with warnings
- Charts using matplotlib
- A web UI with Flask or a desktop UI with Tkinter

## License
MIT
