# This is a Budgeting Simulator, built with NumPy to handle your finances in a simple fashion.
#
# Within this program you will find NumPy array creation, indexing, slicing,
# appending, statistics, and JSON reporting.

from datetime import datetime
import json
import numpy as np

categories = ["Income", "Expenses", "Savings", "Investments"]
account_types = {
    "Income": "income",
    "Expenses": "expense",
    "Savings": "savings",
    "Investments": "investment",
}

# Start with three named accounts and no transactions. New transactions are
# appended as columns when the user chooses "Add Transaction".
transaction_record = np.empty((len(categories), 0), dtype=float)

# Timestamps stay aligned with transaction_record and start empty as well.
transaction_timestamps = np.empty((len(categories), 0), dtype=object)
activity_log = []


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def record_activity(message):
    entry = f"[{current_timestamp()}] {message}"
    activity_log.append(entry)
    print(entry)


def display_transaction(category, column_index):
    row_index = categories.index(category)
    timestamp = transaction_timestamps[row_index, column_index]
    timestamp_text = (
        timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(timestamp, datetime)
        else "no transaction timestamp"
    )
    print(
        f"{category} transaction {column_index + 1}: "
        f"${transaction_record[row_index, column_index]:.2f} "
        f"({timestamp_text})"
    )


def show_current_stats():
    income_index = categories.index("Income") if "Income" in categories else None
    total_income = np.sum(transaction_record[income_index]) if income_index is not None else 0
    totals = {
        name: np.sum(transaction_record[index])
        for index, name in enumerate(categories)
    }
    total_spent = totals.get("Expenses", 0)
    total_saved = totals.get("Savings", 0)
    total_invested = totals.get("Investments", 0)
    remaining_balance = total_income - total_spent - total_saved - total_invested

    print("\nCurrent Stats")
    print(f"Total Income:     ${total_income:.2f}")
    print(f"Total Expenses:   ${total_spent:.2f}")
    print(f"Total Saved:      ${total_saved:.2f}")
    print(f"Total Invested:   ${total_invested:.2f}")
    print(f"Remaining Balance: ${remaining_balance:.2f}")


def add_transaction():
    global transaction_record, transaction_timestamps

    category = input(f"Category ({', '.join(categories)}): ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return
    if category not in categories:
        print(f"Please choose one of: {', '.join(categories)}.")
        return

    amount_text = input("Amount: ").strip()
    if not amount_text:
        print("Amount cannot be empty.")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount < 0:
        print("Amount cannot be negative.")
        return

    # Like your original np.append calls, add a column while preserving rows.
    new_column = np.zeros((len(categories), 1), dtype=float)
    new_column[categories.index(category), 0] = amount
    transaction_record = np.append(transaction_record, new_column, axis=1)
    timestamp = datetime.now()
    new_timestamp_column = np.full((len(categories), 1), "", dtype=object)
    new_timestamp_column[categories.index(category), 0] = timestamp
    transaction_timestamps = np.append(
        transaction_timestamps, new_timestamp_column, axis=1
    )
    column_index = transaction_record.shape[1] - 1
    print(f"Added ${amount:.2f} to {category}.")
    display_transaction(category, column_index)
    record_activity(
        f"Added ${amount:.2f} to {category} ({account_types[category]} account, "
        f"transaction {column_index + 1})."
    )


def edit_recent_transaction():
    """Edit one of the selected account's last two transactions."""
    global transaction_timestamps

    if transaction_record.shape[1] == 0:
        print("There are no transactions to edit. Add a transaction first.")
        return

    category = input(f"Account to edit ({', '.join(categories)}): ").strip().title()
    if category not in categories:
        print("That account does not exist.")
        return

    transaction_count = transaction_record.shape[1]
    first_recent = max(0, transaction_count - 2)
    print("\nLast two transactions:")
    for column_index in range(first_recent, transaction_count):
        display_transaction(category, column_index)

    selection_text = input(
        f"Transaction number to edit ({first_recent + 1}-{transaction_count}): "
    ).strip()
    try:
        selected_number = int(selection_text)
    except ValueError:
        print("Invalid transaction number.")
        return
    if selected_number < first_recent + 1 or selected_number > transaction_count:
        print("Please choose one of the displayed transaction numbers.")
        return

    amount_text = input("New amount: ").strip()
    try:
        new_amount = float(amount_text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    if new_amount < 0:
        print("Amount cannot be negative.")
        return

    row_index = categories.index(category)
    column_index = selected_number - 1
    old_amount = transaction_record[row_index, column_index]
    transaction_record[row_index, column_index] = new_amount
    transaction_timestamps[row_index, column_index] = datetime.now()
    print(f"Updated {category} transaction {selected_number}.")
    display_transaction(category, column_index)
    record_activity(
        f"Edited {category} transaction {selected_number}: "
        f"${old_amount:.2f} -> ${new_amount:.2f}."
    )


def run_scenario():
    """Apply a percentage change to every transaction in one category row."""
    global transaction_timestamps
    category = input(f"Category to change ({', '.join(categories)}): ").strip().title()
    if not category:
        print("Category cannot be empty.")
        return
    if category not in categories:
        print(f"Please choose one of: {', '.join(categories)}.")
        return

    percentage_text = input("Percentage change (for example, 10 or -5): ").strip()
    if not percentage_text:
        print("Percentage cannot be empty.")
        return

    try:
        percentage = float(percentage_text)
    except ValueError:
        print("Invalid percentage. Please enter a number.")
        return

    row_index = categories.index(category)
    multiplier = 1 + (percentage / 100)
    transaction_record[row_index, :] *= multiplier
    print(f"Applied a {percentage:g}% change to {category}.")
    transaction_timestamps[row_index, :] = datetime.now()
    record_activity(f"Applied a {percentage:g}% scenario to {category}.")


def analyze_spending():
    spending_indices = [
        index for index, name in enumerate(categories)
        if account_types[name] == "expense"
    ]
    spending = transaction_record[spending_indices, :].flatten()
    if spending.size == 0:
        print("There are no spending transactions to analyze.")
        return

    print("\nSpending Analysis")
    print(f"Mean spending: ${np.mean(spending):.2f}")
    print(f"Spending standard deviation: ${np.std(spending):.2f}")


def calculate_investment_growth():
    """Estimate compound growth for the current Investments account."""
    if "Investments" not in categories:
        print("Add an Investments account before using this calculator.")
        return

    investment_index = categories.index("Investments")
    principal = float(np.sum(transaction_record[investment_index]))
    print(f"Current investment balance: ${principal:.2f}")

    rate_text = input("Expected annual return percentage: ").strip()
    years_text = input("Number of years: ").strip()
    contribution_text = input("Monthly contribution (press Enter for 0): ").strip()
    if not rate_text or not years_text:
        print("Annual return and years cannot be empty.")
        return

    try:
        annual_rate = float(rate_text) / 100
        years = float(years_text)
        monthly_contribution = float(contribution_text) if contribution_text else 0
    except ValueError:
        print("Please enter valid numbers for the investment calculation.")
        return
    if years < 0 or monthly_contribution < 0:
        print("Years and monthly contributions cannot be negative.")
        return

    # Compound growth: principal grows annually and monthly contributions grow
    # at the equivalent monthly rate using NumPy arithmetic.
    months = years * 12
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        future_value = principal + (monthly_contribution * months)
    else:
        growth_factor = (1 + monthly_rate) ** months
        future_value = (principal * growth_factor) + (
            monthly_contribution * ((growth_factor - 1) / monthly_rate)
        )

    print(f"Estimated investment value after {years:g} years: ${future_value:.2f}")
    record_activity(
        f"Calculated Investments growth from ${principal:.2f} to "
        f"${future_value:.2f} over {years:g} years."
    )


def show_activity_log():
    print("\nActivity Log")
    if not activity_log:
        print("No changes have been made during this session.")
        return
    for entry in activity_log:
        print(entry)


def build_monthly_report():
    """Build a JSON-ready report describing transaction behavior by month."""
    monthly_data = {}

    for row_index, category in enumerate(categories):
        for column_index in range(transaction_record.shape[1]):
            timestamp = transaction_timestamps[row_index, column_index]
            amount = transaction_record[row_index, column_index]
            if not isinstance(timestamp, datetime) or amount == 0:
                continue

            month = timestamp.strftime("%Y-%m")
            month_data = monthly_data.setdefault(
                month,
                {"categories": {}, "total_income": 0.0, "total_allocated": 0.0},
            )
            category_data = month_data["categories"].setdefault(
                category,
                {"account_type": account_types[category], "amounts": []},
            )
            category_data["amounts"].append(float(amount))

    for month_data in monthly_data.values():
        for category_data in month_data["categories"].values():
            amounts = np.array(category_data.pop("amounts"), dtype=float)
            category_data["transaction_count"] = int(amounts.size)
            category_data["total"] = round(float(np.sum(amounts)), 2)
            category_data["average"] = round(float(np.mean(amounts)), 2)
            category_data["highest"] = round(float(np.max(amounts)), 2)
            category_data["lowest"] = round(float(np.min(amounts)), 2)

        for category, category_data in month_data["categories"].items():
            if account_types[category] == "income":
                month_data["total_income"] += category_data["total"]
            else:
                month_data["total_allocated"] += category_data["total"]

        month_data["total_income"] = round(month_data["total_income"], 2)
        month_data["total_allocated"] = round(month_data["total_allocated"], 2)
        month_data["net_cash_flow"] = round(
            month_data["total_income"] - month_data["total_allocated"], 2
        )
        if month_data["categories"]:
            largest_category = max(
                month_data["categories"],
                key=lambda name: month_data["categories"][name]["total"],
            )
            month_data["largest_account_activity"] = largest_category

    months = sorted(monthly_data)
    report = {
        "report_name": "The Budget Simulator - Monthly Behavior Report",
        "generated_at": current_timestamp(),
        "months_included": months,
        "months": monthly_data,
        "insights": {
            "most_active_month": max(
                months,
                key=lambda month: sum(
                    data["transaction_count"]
                    for data in monthly_data[month]["categories"].values()
                ),
                default=None,
            ),
            "note": (
                "Net cash flow equals income minus expenses, savings, and investments."
            ),
        },
    }
    return report


def show_monthly_report():
    report = build_monthly_report()
    if not report["months_included"]:
        print("\nNo timestamped transactions are available for a monthly report.")
        return

    print("\nMonthly Behavior Report (JSON)")
    print(json.dumps(report, indent=2))
    record_activity(
        f"Generated a monthly JSON report for {len(report['months_included'])} month(s)."
    )


def add_account():
    global categories, transaction_record, transaction_timestamps

    account = input("New account name: ").strip().title()
    if not account:
        print("Account name cannot be empty.")
        return
    if account in categories:
        print("That account already exists.")
        return

    account_type = input(
        "Account type (income, expense, savings, investment): "
    ).strip().lower()
    valid_types = {"income", "expense", "savings", "investment"}
    if account_type not in valid_types:
        print("Please choose income, expense, savings, or investment.")
        return

    categories.append(account)
    account_types[account] = account_type
    new_row = np.zeros((1, transaction_record.shape[1]), dtype=float)
    # Adding axis=0 appends a new account while keeping transaction columns aligned.
    transaction_record = np.append(transaction_record, new_row, axis=0)
    new_timestamp_row = np.full((1, transaction_timestamps.shape[1]), "", dtype=object)
    transaction_timestamps = np.append(transaction_timestamps, new_timestamp_row, axis=0)
    print(f"Added the {account} {account_type} account with a zero balance.")
    record_activity(f"Added the {account} {account_type} account.")


def remove_account():
    global categories, transaction_record, transaction_timestamps

    account = input(f"Account to remove ({', '.join(categories)}): ").strip().title()
    if account not in categories:
        print("That account does not exist.")
        return
    if len(categories) == 1:
        print("At least one account must remain.")
        return

    row_index = categories.index(account)
    categories.pop(row_index)
    account_type = account_types.pop(account)
    transaction_record = np.delete(transaction_record, row_index, axis=0)
    transaction_timestamps = np.delete(transaction_timestamps, row_index, axis=0)
    print(f"Removed the {account} account and its transactions.")
    record_activity(
        f"Removed the {account} {account_type} account and its transactions."
    )


def clear_account():
    global transaction_timestamps

    account = input(f"Account to clear ({', '.join(categories)}): ").strip().title()
    if account not in categories:
        print("That account does not exist.")
        return

    row_index = categories.index(account)
    transaction_record[row_index, :] = 0
    transaction_timestamps[row_index, :] = datetime.now()
    print(f"Cleared all transactions in the {account} account.")
    record_activity(f"Cleared all transactions in the {account} account.")


def main():
    while True:
        print("\n=== The Budget Simulator ===")
        print("1. View Current Stats")
        print("2. Add Transaction")
        print("3. Run Scenario")
        print("4. Calculate Investment Growth")
        print("5. Analyze Expenses")
        print("6. Edit One of the Last Two Transactions")
        print("7. Add Account")
        print("8. Remove Account")
        print("9. Clear Account Balance")
        print("10. View Activity Log")
        print("11. Generate Monthly JSON Report")
        print("12. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_current_stats()
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            run_scenario()
        elif choice == "4":
            calculate_investment_growth()
        elif choice == "5":
            analyze_spending()
        elif choice == "6":
            edit_recent_transaction()
        elif choice == "7":
            add_account()
        elif choice == "8":
            remove_account()
        elif choice == "9":
            clear_account()
        elif choice == "10":
            show_activity_log()
        elif choice == "11":
            show_monthly_report()
        elif choice == "12":
            print("Goodbye!")
            break
        elif not choice:
            print("Please enter a menu option.")
        else:
            print("Invalid option. Choose a number from 1 to 12.")

if __name__ == "__main__":
    main()

