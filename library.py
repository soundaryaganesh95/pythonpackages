# The main data structure: a dictionary where the key is the book title (string)
# and the value is the number of copies available (integer).
library_inventory = {
    "The Great Gatsby": 3,
    "1984": 2,
    "Pride and Prejudice": 4,
    "Moby Dick": 0 # Example of a book with no copies available
}

def view_available_books():
    """Views all books and their availability status."""
    if not library_inventory:
        print("\n*** 📚 The library is empty! ***")
        return

    print("\n--- Available Books ---")
    print(f"{'Title':<30} | {'Copies Available':<16}")
    print("-" * 48)

    # Iterating through the dictionary
    for title, copies in library_inventory.items():
        status = " (Out of Stock)" if copies == 0 else ""
        print(f"{title:<30} | {copies:<16}{status}")
    print("-" * 48)

# --------------------------------------------------

def add_book():
    """Adds a new book or increases the count of an existing book."""
    title = input("Enter the title of the book to add: ").strip().title()
    
    if not title:
        print("❌ Title cannot be empty.")
        return

    while True:
        try:
            quantity = int(input(f"Enter the number of copies of '{title}' to add: "))
            if quantity >= 0:
                break
            else:
                print("Quantity must be a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Adding or Updating Dictionary Items
    if title in library_inventory:
        library_inventory[title] += quantity
        print(f"✅ Added {quantity} copies. Total copies of '{title}': {library_inventory[title]}.")
    else:
        library_inventory[title] = quantity
        print(f"✅ Book '{title}' added to the inventory with {quantity} copies.")

# --------------------------------------------------

def borrow_book():
    """Borrows a book if copies are available."""
    title = input("Enter the title of the book to BORROW: ").strip().title()

    # Accessing Dictionary Items
    if title not in library_inventory:
        print(f"❌ Book '{title}' is not in the library collection.")
        return

    current_copies = library_inventory[title]
    
    if current_copies > 0:
        # Updating Dictionary Items
        library_inventory[title] -= 1
        print(f"✅ You have borrowed '{title}'. Copies left: {library_inventory[title]}")
    else:
        print(f"⚠️ Sorry, all copies of '{title}' are currently borrowed.")

# --------------------------------------------------

def return_book():
    """Returns a book, increasing the available count."""
    title = input("Enter the title of the book to RETURN: ").strip().title()

    # Accessing Dictionary Items
    if title not in library_inventory:
        # Option: If the user returns a book not in the system, add it back with 1 copy.
        add_new = input(f"Book '{title}' not found. Add it to inventory with 1 copy? (y/n): ").lower().strip()
        if add_new == 'y':
            library_inventory[title] = 1
            print(f"✅ '{title}' returned and added to inventory (1 copy).")
        else:
            print("Return canceled.")
        return
    
    # Updating Dictionary Items
    library_inventory[title] += 1
    print(f"✅ Thank you! '{title}' has been returned. Copies available: {library_inventory[title]}")

# --------------------------------------------------

def main_menu():
    """Main function to run the library management system."""
    while True:
        print("\n*** 🏛️ Library Management System ***")
        print("1. View Available Books")
        print("2. Add/Stock Books")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            view_available_books()
        elif choice == '2':
            add_book()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            print("Exiting Library System. Have a great day! 👋")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Run the main program
if __name__ == "__main__":
    main_menu()