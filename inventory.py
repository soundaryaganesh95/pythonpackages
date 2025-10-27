import json
import os
import time 

# --- Configuration ---
DATA_FILE = "inventory_data.json"

# --- Data Persistence Functions ---

def _load_data():
    """Loads all system data (products and earnings) from the JSON file."""
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        # Initial empty structure
        return {
            "products": [],
            "total_earnings": 0.0,
            "next_product_id": 1001
        }
    
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Warning: {DATA_FILE} is corrupted. Initializing new system data.")
            return {
                "products": [],
                "total_earnings": 0.0,
                "next_product_id": 1001
            }

def _save_data(data):
    """Saves all system data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Classes ---

class Product:
    """Represents a Product in the inventory system."""
    def __init__(self, product_id, name, price, quantity):
        self.id = product_id
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }
    
    def __str__(self):
        return f"{self.name} (ID: {self.id}) | Price: ${self.price:,.2f} | Stock: {self.quantity}"

# --- Core Management System ---

class InventorySystem:
    def __init__(self):
        self.data = _load_data()
        # Re-create Product objects from stored data
        self.products = [Product(**p) for p in self.data["products"]]
        self.total_earnings = self.data["total_earnings"]
        
    def _save_state(self):
        """Prepares and saves the current state to the JSON file."""
        # Convert Product objects back to dictionaries for storage
        self.data["products"] = [p.to_dict() for p in self.products]
        self.data["total_earnings"] = self.total_earnings
        _save_data(self.data)
        
    def add_product(self, name, price, quantity):
        """Adds a new product or restocks an existing one."""
        
        # Check if product already exists by name
        existing_product = next((p for p in self.products if p.name.lower() == name.lower()), None)
        
        if existing_product:
            existing_product.quantity += quantity
            print(f"✅ Product already exists. Stock updated for '{name}'. New quantity: {existing_product.quantity}")
        else:
            product_id = self.data["next_product_id"]
            new_product = Product(product_id, name, price, quantity)
            self.products.append(new_product)
            self.data["next_product_id"] += 1
            print(f"✅ New product '{name}' added with ID: {product_id}")
            
        self._save_state()

    def show_inventory(self):
        """Displays all available products and their stock."""
        if not self.products:
            print("\n⚠️ Inventory is empty. Please add some products.")
            return

        print("\n--- 📦 Current Stock Inventory ---")
        for prod in self.products:
            print(f"  {prod}")
        print("-" * 50)

    def process_purchase(self):
        """Handles the purchase of a product, decreasing quantity and updating earnings."""
        self.show_inventory()
        if not self.products:
            return

        # 1. Select Product
        selected_product = None
        while selected_product is None:
            try:
                prod_id_input = input("Enter Product ID to purchase (or 'q' to cancel): ").strip()
                if prod_id_input.lower() == 'q': return
                
                prod_id = int(prod_id_input)
                selected_product = next((p for p in self.products if p.id == prod_id), None)
                
                if not selected_product:
                    print("❌ Invalid Product ID.")
            except ValueError:
                print("❌ Invalid input. Please enter a number or 'q'.")

        # 2. Select Quantity
        quantity_to_buy = 0
        while True:
            try:
                quantity_input = input(f"Enter quantity for '{selected_product.name}' (Max: {selected_product.quantity}): ").strip()
                if not quantity_input: return # Allow canceling
                
                quantity_to_buy = int(quantity_input)
                
                if quantity_to_buy <= 0:
                    print("❌ Quantity must be positive.")
                elif quantity_to_buy > selected_product.quantity:
                    print(f"❌ Insufficient stock. Only {selected_product.quantity} available.")
                else:
                    break
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
        
        # 3. Process Transaction
        sale_amount = quantity_to_buy * selected_product.price
        
        # Update stock and earnings
        selected_product.quantity -= quantity_to_buy
        self.total_earnings += sale_amount
        
        self._save_state()
        
        print(f"\n🎉 Purchase Successful!")
        print(f"  Item: {selected_product.name}")
        print(f"  Quantity: {quantity_to_buy}")
        print(f"  Total Cost: ${sale_amount:,.2f}")
        print(f"  Remaining Stock: {selected_product.quantity}")

    def show_summary(self):
        """Displays the total available stock value and total earnings."""
        # Calculate the total value of remaining inventory
        total_stock_value = sum(p.price * p.quantity for p in self.products)

        print("\n--- 💰 Financial Summary ---")
        print(f"Total Earnings (from sales): ${self.total_earnings:,.2f}")
        print(f"Total Current Stock Value:   ${total_stock_value:,.2f}")
        print("-" * 35)

# --- Main CLI Application Helper Functions ---

def get_valid_float(prompt):
    """Helper function to get and validate a non-negative float."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value >= 0:
                return value
            else:
                print("Value must be zero or positive.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_int(prompt):
    """Helper function to get and validate a non-negative integer."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= 0:
                return value
            else:
                print("Quantity must be zero or positive.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def main():
    """Runs the main command-line interface for the Inventory Management System."""
    system = InventorySystem()
    print("Welcome to the Store Inventory Management System.")
    
    # Initialize with default products if system is empty
    if not system.products:
        print("Initializing with some default inventory data...")
        # Note: add_product calls _save_state internally
        system.add_product("Laptop Pro", 1200.00, 5)
        system.add_product("Wireless Mouse", 25.50, 50)
    
    while True:
        print("\n*** IMS Main Menu ***")
        print("1. Add/Restock Product")
        print("2. Process Purchase")
        print("3. Show Available Stock")
        print("4. Show Financial Summary")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            name = input("Product Name: ").strip()
            # Use helper functions for validation
            price = get_valid_float("Unit Price: $")
            quantity = get_valid_int("Initial/Restock Quantity: ")
            
            if name and price is not None and quantity is not None:
                system.add_product(name, price, quantity)
            else:
                print("❌ All fields are required.")

        elif choice == '2':
            system.process_purchase()

        elif choice == '3':
            system.show_inventory()

        elif choice == '4':
            system.show_summary()

        elif choice == '5':
            print("Thank you for using the IMS. Goodbye! 👋")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
