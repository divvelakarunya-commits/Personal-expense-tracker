
import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"


# Create CSV file
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "ID", "Date", "Category", "Amount", "Description"
            ])


# Add Expense
def add_expense():
    print("\n--- ADD EXPENSE ---")

    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    description = input("Enter description: ")

    with open(FILE_NAME, "r", newline="") as file:
        rows = list(csv.reader(file))

    expense_id = max(
        (int(row[0]) for row in rows[1:]
         if row and row[0].isdigit()),
        default=0
    ) + 1

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            expense_id,
            date.today(),
            category,
            amount,
            description
        ])

    print("\nExpense added successfully!")


# View Expenses
def view_expenses():
    print("\n--- ALL EXPENSES ---")

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)

        found = False

        for row in reader:
            if row:
                print(
                    "ID:", row[0],
                    "| Date:", row[1],
                    "| Category:", row[2],
                    "| Amount: Rs.", row[3],
                    "| Description:", row[4]
                )
                found = True

        if not found:
            print("No expenses found.")


# Total Expenses
def total_expenses():
    total = 0

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += float(row["Amount"])

    print("\nTotal Expenses: Rs.", round(total, 2))


# Category Summary
def category_summary():
    categories = {}

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["Category"]
            amount = float(row["Amount"])

            categories[category] = (
                categories.get(category, 0) + amount
            )

    print("\n--- CATEGORY SUMMARY ---")

    if not categories:
        print("No expenses found.")
    else:
        for category, amount in categories.items():
            print(category, ": Rs.", round(amount, 2))


# Delete Expense
def delete_expense():
    view_expenses()

    try:
        expense_id = input("\nEnter expense ID to delete: ")

        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        updated_rows = [
            row for row in rows
            if row["ID"] != expense_id
        ]

        if len(updated_rows) == len(rows):
            print("Expense ID not found.")
            return

        with open(FILE_NAME, "w", newline="") as file:
            fieldnames = [
                "ID", "Date", "Category", "Amount", "Description"
            ]

            writer = csv.DictWriter(
                file, fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(updated_rows)

        print("Expense deleted successfully!")

    except (OSError, KeyError) as error:
        print("Error:", error)


# Main Menu
def main():
    create_file()

    while True:

        print("\n================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("================================")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Category Summary")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            total_expenses()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            delete_expense()

        elif choice == "6":
            print("\nThank you for using Personal Expense Tracker!")
            break

        else:
            print("\nInvalid choice! Please try again.")


# Start Program
if __name__ == "__main__":
    main()
