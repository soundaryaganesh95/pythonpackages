# The main data structure: a dictionary where the key is the account PIN (string)
# and the value is the account balance (float).
ACCOUNTS = {
    "1234": 1500.50,  # PIN: 1234, Balance: $1500.50
    "4321": 500.00,   # PIN: 4321, Balance: $500.00
    "9999": 10000.00  # PIN: 9999, Balance: $10000.00
}

# Variable to store the currently logged-in user's PIN
current_pin = None

# --- Core ATM Functions ---

def authenticate():
    """Authenticates the user using a PIN."""
    global current_pin
    
    print("\n--- Welcome to the ATM ---")
    
    for _ in range(3): # Allow 3 attempts
        pin = input("Please enter your 4-digit PIN: ").strip()
        
        # Accessing Dictionary Items: Check if the PIN exists as a key
        if pin in ACCOUNTS:
            current_pin = pin
            print("✅ Authentication successful.")
            return True
        else:
            print("❌ Invalid PIN. Please try again.")
            
    print("🔒 Maximum attempts reached. Card retained.")
    return False

def check_balance():
    """Check balance 🏦"""
    if current_pin is None:
        return
        
    # Accessing Dictionary Items: Retrieve the balance using the PIN
    balance = ACCOUNTS[current_pin]
    print(f"\nYour current balance is: 🏦 ${balance:,.2f}")

def deposit():
    """Deposit money 💰"""
    if current_pin is None:
        return

    while True:
        try:
            amount = float(input("Enter the amount to DEPOSIT: $"))
            if amount > 0:
                # Updating Dictionary Items: Add the deposit amount to the current balance
                ACCOUNTS[current_pin] += amount
                print(f"✅ Successfully deposited ${amount:,.2f}.")
                check_balance()
                break
            else:
                print("Amount must be positive.")
        except ValueError:
            print("Invalid input. Please enter a numerical amount.")

def withdraw():
    """Withdraw money 💸"""
    if current_pin is None:
        return
        
    current_balance = ACCOUNTS[current_pin]

    while True:
        try:
            amount = float(input("Enter the amount to WITHDRAW: $"))
            
            if amount <= 0:
                print("Amount must be positive.")
            elif amount > current_balance:
                print(f"❌ Insufficient funds. Your current balance is ${current_balance:,.2f}.")
            else:
                # Updating Dictionary Items: Subtract the withdrawal amount
                ACCOUNTS[current_pin] -= amount
                print(f"✅ Successfully withdrew ${amount:,.2f}.")
                check_balance()
                break
        except ValueError:
            print("Invalid input. Please enter a numerical amount.")

def main_menu():
    """Displays the main menu and handles user selection."""
    while True:
        print("\n--- ATM Transaction Menu ---")
        print("1. Check Balance 🏦")
        print("2. Deposit Money 💰")
        print("3. Withdraw Money 💸")
        print("4. Exit and Log Out")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            check_balance()
        elif choice == '2':
            deposit()
        elif choice == '3':
            withdraw()
        elif choice == '4':
            print("👋 Thank you for using this ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# --------------------------------------------------

def start_atm():
    """Initializes and runs the ATM sequence."""
    if authenticate():
        main_menu()

# Run the main program
if __name__ == "__main__":
    start_atm()