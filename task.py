import abc # Needed for Abstract Base Classes
import os
import json # Needed for Mini-Project file storage

# ====================================================================
# Task 1-3: Class, Object, Methods, Constructor
# ====================================================================

class Car:
    # Class attribute to track the number of Car objects (for demonstration)
    car_count = 0 
    
    # Task 3: Constructor (__init__ method)
    def __init__(self, brand, model, year):
        # Task 1: Attributes
        self.brand = brand
        self.model = model
        self.year = year
        Car.car_count += 1

    # Task 2: Add Methods to a Class
    def start_engine(self):
        print(f"[{self.brand} {self.model}] Engine started! Vroom!")

    def get_details(self):
        # Task 1: Access object details
        print(f"Car Details: {self.year} {self.brand} {self.model}")

# Task 1 & 2: Creating objects and calling methods
my_car = Car("Toyota", "Camry", 2020)
print("\n--- Task 1 & 2: Basic Class and Method ---")
my_car.get_details()
my_car.start_engine()

# Task 3: Creating multiple objects
new_car = Car("Ford", "Mustang", 1969)
new_car.get_details()
print(f"Total cars created: {Car.car_count}")

# ====================================================================
# Task 4 & 11: Encapsulation and File Handling
# ====================================================================

class BankAccount:
    def __init__(self, owner, initial_balance=0):
        # Task 4: Private attribute (Encapsulation)
        self.__balance = initial_balance
        self.owner = owner
        self.filename = f"{owner}_transactions.txt"
        self._initialize_file()

    def _initialize_file(self):
        """Helper to ensure the file exists and record initial balance."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write(f"Initial Balance: {self.__balance:.2f}\n")

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self._save_transaction(f"Deposit: +{amount:.2f}")
            print(f"Deposit successful. New balance: ${self.__balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self._save_transaction(f"Withdrawal: -{amount:.2f}")
            print(f"Withdrawal successful. New balance: ${self.__balance:.2f}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        # Access method to check the private balance
        print(f"Current balance for {self.owner}: ${self.__balance:.2f}")
    
    # Task 11: File Handling - Saving transactions
    def _save_transaction(self, transaction_details):
        with open(self.filename, 'a') as f:
            f.write(transaction_details + "\n")
            
    # Task 11: File Handling - Reading history
    def read_history(self):
        print(f"\n--- Transaction History for {self.owner} ---")
        try:
            with open(self.filename, 'r') as f:
                print(f.read().strip())
        except FileNotFoundError:
            print("No transaction history found.")
        print("------------------------------------------")

print("\n--- Task 4 & 11: Encapsulation & File Handling ---")
account = BankAccount("Alice", 500)
account.check_balance()
account.deposit(100.50)
account.withdraw(50)
# Attempting direct access (name mangling applied, but still not recommended)
# print(f"Direct (mangled) access attempt: {account._BankAccount__balance}")
account.read_history()

# ====================================================================
# Task 5 & 6: Inheritance & Method Overriding (Polymorphism)
# ====================================================================

# Task 5: Parent Class
class Vehicle:
    def __init__(self, manufacturer):
        self.manufacturer = manufacturer
    
    # Task 5: show_details() method
    def show_details(self):
        print(f"Vehicle: Manufacturer is {self.manufacturer}.")

# Task 5: Child Class (Inherits from Vehicle)
class Sedan(Vehicle):
    def __init__(self, manufacturer, seats, color):
        super().__init__(manufacturer)
        self.seats = seats
        self.color = color
    
    # Task 6: Method Overriding (Polymorphism)
    def show_details(self):
        # Calling the parent method is optional but good practice
        super().show_details() 
        print(f"  Type: Sedan | Seats: {self.seats} | Color: {self.color}")

print("\n--- Task 5 & 6: Inheritance & Overriding ---")
my_vehicle = Vehicle("Generic Motors")
my_vehicle.show_details()

my_sedan = Sedan("Honda", 4, "Blue")
my_sedan.show_details() # Calls the overridden method

# ====================================================================
# Task 7: Multiple Inheritance
# ====================================================================

class Teacher:
    def teach(self):
        return "I am teaching a class."
    def work(self):
        return self.teach()

class Researcher:
    def research(self):
        return "I am conducting research."
    def work(self):
        return self.research() # Overridden from Teacher

# Professor inherits from both
class Professor(Teacher, Researcher):
    def work(self):
        # Method Resolution Order (MRO) will choose Teacher's work() first
        return f"As a Professor, I can say: {Teacher.work(self)} AND {Researcher.work(self)}"

print("\n--- Task 7: Multiple Inheritance ---")
professor = Professor()
print(professor.work())
# print(Professor.__mro__) # MRO: (Professor, Teacher, Researcher, object)

# ====================================================================
# Task 8: Abstract Class & Method
# ====================================================================

# Abstract Class
class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self):
        # Abstract method has no implementation
        pass

# Implementation Subclass 1
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    # Must implement the abstract method area()
    def area(self):
        return 3.14159 * self.radius * self.radius

# Implementation Subclass 2
class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
        
    def area(self):
        return self.length * self.width

print("\n--- Task 8: Abstract Class & Method ---")
circ = Circle(5)
rect = Rectangle(4, 6)
print(f"Circle Area (r=5): {circ.area():.2f}")
print(f"Rectangle Area (4x6): {rect.area()}")

# ====================================================================
# Task 9: Operator Overloading
# ====================================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    # Overload the + operator using the __add__ dunder method
    def __add__(self, other):
        # Returns a new Vector object
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

print("\n--- Task 9: Operator Overloading ---")
v1 = Vector(2, 5)
v2 = Vector(3, -1)
v3 = v1 + v2 # Calls v1.__add__(v2)
print(f"Vector 1: {v1}")
print(f"Vector 2: {v2}")
print(f"Vector 3 (v1 + v2): {v3}")

# ====================================================================
# Task 10: Class Method & Static Method
# ====================================================================

class Person:
    # Class attribute to track object count
    number_of_people = 0 
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        # Increment count using the class method
        self.count_people() 
        
    # Task 10: Class Method (uses the class itself as the first argument, 'cls')
    @classmethod
    def count_people(cls):
        cls.number_of_people += 1
        return cls.number_of_people

    # Task 10: Static Method (does not receive 'self' or 'cls', acts like a regular function)
    @staticmethod
    def is_adult(age):
        return age >= 18

print("\n--- Task 10: Class Method & Static Method ---")
p1 = Person("Jenna", 25)
p2 = Person("Kyle", 16)

# Accessing the class attribute directly
print(f"Total Person objects created (via attribute): {Person.number_of_people}") 

# Calling the static method
print(f"Is Jenna (age {p1.age}) an adult? {Person.is_adult(p1.age)}")
print(f"Is Kyle (age {p2.age}) an adult? {Person.is_adult(p2.age)}")


# ====================================================================
# Task 12: Mini Project - Student Management System
# ====================================================================

class Student:
    def __init__(self, name, age, marks):
        self.name = name
        self.age = age
        self.marks = marks # Dictionary: {"subject": score}

    # Add student details (done via constructor here, but method allows updates)
    def add_marks(self, subject, score):
        # Adding/Updating Dictionary Items
        self.marks[subject] = score
        print(f"Added/Updated {subject} marks for {self.name}.")

    # Update student marks (similar to add_marks, focusing on modification)
    def update_marks(self, subject, new_score):
        if subject in self.marks:
            self.marks[subject] = new_score
            print(f"Updated {self.name}'s {subject} score to {new_score}.")
        else:
            print(f"{self.name} is not enrolled in {subject}. Use add_marks().")

    # Display student details
    def display_details(self):
        print("\n--- Student Details ---")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print("Marks:")
        # Iterating Through a Dictionary
        for subj, score in self.marks.items():
            print(f"  - {subj}: {score}")
        print("-----------------------")

print("\n--- Task 12: Mini Project - Student System ---")
student1 = Student("Michael", 18, {"Math": 85, "Physics": 78})
student1.display_details()
student1.add_marks("Chemistry", 92)
student1.update_marks("Physics", 85)
student1.display_details()

# ====================================================================
# Task 13: Mini Project - Employee Payroll System
# ====================================================================

class Employee:
    def __init__(self, name, emp_id, salary):
        self.name = name
        self.id = emp_id
        self.salary = salary # Monthly salary
        self.file_path = "employee_data.json"

    def calculate_net_salary(self, tax_rate=0.15):
        """Calculate Salary after tax deductions."""
        tax = self.salary * tax_rate
        net_salary = self.salary - tax
        return net_salary

    def give_raise(self, percentage):
        """Give a raise based on a percentage."""
        raise_amount = self.salary * (percentage / 100)
        self.salary += raise_amount
        print(f"✅ {self.name} received a {percentage}% raise. New salary: ${self.salary:,.2f}")

    def store_details(self):
        """Store employee details in a file (JSON format)."""
        data = {
            "name": self.name,
            "id": self.id,
            "salary": self.salary,
            "net_salary": self.calculate_net_salary()
        }
        
        # Read existing data if file exists
        all_employees = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try:
                    all_employees = json.load(f)
                except json.JSONDecodeError:
                    pass # File is empty or corrupt
        
        # Add/update the current employee's data
        all_employees[self.id] = data
        
        # Write back to file
        with open(self.file_path, 'w') as f:
            json.dump(all_employees, f, indent=4)
            
        print(f"✅ Employee details for {self.name} stored/updated in {self.file_path}.")

print("\n--- Task 13: Mini Project - Employee System ---")
emp1 = Employee("Barbara Gordon", "E001", 60000)
net_salary = emp1.calculate_net_salary()
print(f"{emp1.name}'s monthly gross salary: ${emp1.salary:,.2f}")
print(f"{emp1.name}'s net salary (after 15% tax): ${net_salary:,.2f}")
emp1.give_raise(5)
emp1.store_details()