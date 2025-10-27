import json
import os
from datetime import datetime

# Define the file path for data storage
DATA_FILE = "finance_data.json"

# ====================================================================
# Core Logic Functions (The "Module" Logic)
# ====================================================================

def _load_data():
    """Loads all transaction data from the JSON file."""
    # Check if the file exists and is not empty
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"transactions": []}
    
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Handle case where file is corrupted or invalid JSON
            print(f"⚠️ Warning: {DATA_FILE} is corrupted. Starting with empty data.")
            return {"transactions": []}

def _save_data(data):
    """Saves all transaction data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_transaction(type, amount, description):
    """
    Allows users to add income and expenses.
    :param type: 'income' or 'expense'
    """
    if amount <= 0:
        print("❌ Transaction amount must be positive.")
        return False
        
    data = _load_data()
    
    new_transaction = {
        "id": len(data["transactions"]) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": type,
        "amount": amount,
        "description": description
    }
    
    data["transactions"].append(new_transaction)
    _save_data(data)
    print(f"✅ {type.title()} transaction recorded successfully.")
    return True

def get_summary():
    """Calculates the total income, total expenses, and net balance."""
    data = _load_data()
    
    total_income = 0.0
    total_expenses = 0.0
    
    for t in data["transactions"]:
        if t["type"] == "income":
            total_income += t["amount"]
        elif t["type"] == "expense":
            total_expenses += t["amount"]
            
    net_balance = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "total_transactions": len(data["transactions"])
    }

def display_summary():
    """Displays a summary of their financial status."""
    summary = get_summary()
    
    net_status = "🟢 Positive" if summary["net_balance"] >= 0 else "🔴 Negative"
    
    print("\n\n--- 📊 Financial Summary ---")
    print(f"Total Income:         +${summary['total_income']:,.2f}")
    print(f"Total Expenses:       -${summary['total_expenses']:,.2f}")
    print("---------------------------------")
    print(f"Net Balance:          ${summary['net_balance']:,.2f} ({net_status})")
    print(f"Total Transactions:   {summary['total_transactions']}")
    print("---------------------------------")

# ====================================================================
# User Interface / Main Application Logic
# ====================================================================

def get_valid_amount():
    """Helper function to get and validate a numerical amount."""
    while True:
        try:
            amount = float(input("Enter amount: $"))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def handle_add_transaction_input(type):
    """Handles user interaction for adding income or expense."""
    print(f"\n--- Add {type.title()} ---")
    amount = get_valid_amount()
    description = input("Enter description (e.g., Salary, Groceries): ").strip()
    
    if description:
        add_transaction(type, amount, description)
    else:
        print("❌ Description cannot be empty. Transaction canceled.")

def main_menu():
    """Main function to run the Personal Finance Tracker."""
    while True:
        print("\n*** 💰 Personal Finance Tracker ***")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            handle_add_transaction_input("income")
        elif choice == '2':
            handle_add_transaction_input("expense")
        elif choice == '3':
            display_summary()
        elif choice == '4':
            print("Exiting tracker. Have a financially fit day! 👋")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Run the main program
if __name__ == "__main__":
    main_menu()