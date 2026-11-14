
import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"


# Create CSV file if it does not exist
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Amount", "Description"])


# Add a new expense
def add_expense():
    try:
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        with open(FILE_NAME, "r", newline="") as file:
            rows = list(csv.reader(file))

        expense_id = len(rows)

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                expense_id,
                date.today(),
                category,
                amount,
                description
            ])

        print("Expense added successfully!")

    except ValueError:
        print("Please enter a valid amount.")


# Display all expenses
def view_expenses():
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("No expenses found.")
        return

    print("\n--- All Expenses ---")
    for row in rows:
        print(" | ".join(row))


# Calculate total expenses
def total_expenses():
    total = 0

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total += float(row["Amount"])

    print("Total Expenses: Rs.", round(total, 2))


# Display category-wise expenses
def category_summary():
    categories = {}

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            category = row["Category"]
            amount = float(row["Amount"])

            categories[category] = categories.get(category, 0) + amount

    print("\n--- Category Summary ---")

    if not categories:
        print("No expenses found.")
    else:
        for category, amount in categories.items():
            print(category, ":", round(amount, 2))


# Delete an expense
def delete_expense():
    view_expenses()

    try:
        expense_id = input("\nEnter expense ID to delete: ")

        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        updated_rows = [
            row for row in rows if row["ID"] != expense_id
        ]

        if len(updated_rows) == len(rows):
            print("Expense ID not found.")
            return

        with open(FILE_NAME, "w", newline="") as file:
            fieldnames = [
                "ID", "Date", "Category", "Amount", "Description"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        print("Expense deleted successfully!")

    except Exception as e:
        print("Error:", e)


# Main menu
def main():
    create_file()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Category Summary")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Enter your choice: ")

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
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
