"""Personal Expense Tracker - a simple command-line app using SQLite.

Usage examples:
    python expense_tracker.py add 250 Food "Lunch with friends"
    python expense_tracker.py add 1200 Transport "Train ticket" --date 2026-11-10
    python expense_tracker.py list
    python expense_tracker.py list --category Food --month 2026-11
    python expense_tracker.py summary --month 2026-11
    python expense_tracker.py delete 3
    python expense_tracker.py export expenses.csv
"""

import argparse
import csv
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

DB_FILE = Path(__file__).with_name("expenses.db")


def get_connection():
    """Open the database and make sure the table exists."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL NOT NULL CHECK (amount > 0),
            category    TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            spent_on    TEXT NOT NULL
        )
        """
    )
    return conn


def valid_date(text):
    """argparse type: accept YYYY-MM-DD only."""
    try:
        return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{text}'. Use YYYY-MM-DD.")


def valid_month(text):
    """argparse type: accept YYYY-MM only."""
    try:
        return datetime.strptime(text, "%Y-%m").strftime("%Y-%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid month '{text}'. Use YYYY-MM.")


def positive_amount(text):
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{text}' is not a number.")
    if value <= 0:
        raise argparse.ArgumentTypeError("Amount must be greater than zero.")
    return round(value, 2)


# ----------------------------- commands -----------------------------------

def add_expense(args):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO expenses (amount, category, description, spent_on) "
            "VALUES (?, ?, ?, ?)",
            (args.amount, args.category.title(), args.description, args.date),
        )
    print(f"Added expense #{cur.lastrowid}: {args.amount:.2f} "
          f"[{args.category.title()}] on {args.date}")


def build_filter(args):
    """Build a WHERE clause from the optional --category / --month flags."""
    clauses, params = [], []
    if getattr(args, "category", None):
        clauses.append("category = ? COLLATE NOCASE")
        params.append(args.category)
    if getattr(args, "month", None):
        clauses.append("substr(spent_on, 1, 7) = ?")
        params.append(args.month)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    return where, params


def list_expenses(args):
    where, params = build_filter(args)
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT * FROM expenses {where} ORDER BY spent_on DESC, id DESC",
            params,
        ).fetchall()

    if not rows:
        print("No expenses found.")
        return

    print(f"{'ID':>4}  {'Date':<10}  {'Category':<14}  {'Amount':>10}  Description")
    print("-" * 60)
    for r in rows:
        print(f"{r['id']:>4}  {r['spent_on']:<10}  {r['category']:<14}  "
              f"{r['amount']:>10.2f}  {r['description']}")
    print("-" * 60)
    print(f"{'Total':>32}  {sum(r['amount'] for r in rows):>10.2f}")


def summary(args):
    where, params = build_filter(args)
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT category, COUNT(*) AS n, SUM(amount) AS total "
            f"FROM expenses {where} GROUP BY category ORDER BY total DESC",
            params,
        ).fetchall()

    if not rows:
        print("No expenses found.")
        return

    grand_total = sum(r["total"] for r in rows)
    title = f"Summary for {args.month}" if args.month else "Summary (all time)"
    print(title)
    print(f"{'Category':<14}  {'Count':>5}  {'Total':>10}  {'Share':>6}")
    print("-" * 42)
    for r in rows:
        share = r["total"] / grand_total * 100
        print(f"{r['category']:<14}  {r['n']:>5}  {r['total']:>10.2f}  {share:>5.1f}%")
    print("-" * 42)
    print(f"{'Total':<14}  {'':>5}  {grand_total:>10.2f}")


def delete_expense(args):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (args.id,))
    if cur.rowcount:
        print(f"Deleted expense #{args.id}.")
    else:
        print(f"No expense with id {args.id}.")
        sys.exit(1)


def export_csv(args):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, spent_on, category, amount, description "
            "FROM expenses ORDER BY spent_on, id"
        ).fetchall()
    with open(args.filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "amount", "description"])
        writer.writerows([tuple(r) for r in rows])
    print(f"Exported {len(rows)} expenses to {args.filename}")


# ------------------------------ CLI setup ---------------------------------

def build_parser():
    parser = argparse.ArgumentParser(description="Personal Expense Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a new expense")
    p_add.add_argument("amount", type=positive_amount)
    p_add.add_argument("category")
    p_add.add_argument("description", nargs="?", default="")
    p_add.add_argument("--date", type=valid_date,
                       default=date.today().strftime("%Y-%m-%d"),
                       help="YYYY-MM-DD (default: today)")
    p_add.set_defaults(func=add_expense)

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--category")
    p_list.add_argument("--month", type=valid_month, help="YYYY-MM")
    p_list.set_defaults(func=list_expenses)

    p_sum = sub.add_parser("summary", help="totals by category")
    p_sum.add_argument("--month", type=valid_month, help="YYYY-MM")
    p_sum.set_defaults(func=summary)

    p_del = sub.add_parser("delete", help="delete an expense by id")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=delete_expense)

    p_exp = sub.add_parser("export", help="export all expenses to CSV")
    p_exp.add_argument("filename")
    p_exp.set_defaults(func=export_csv)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
