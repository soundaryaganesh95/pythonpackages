import json
import os
from datetime import datetime

# --- Configuration ---
DATA_FILE = "hospital_data.json"

# --- Data Persistence Functions ---

def _load_data():
    """Loads all system data (doctors, appointments) from the JSON file."""
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        # Initial empty structure
        return {
            "doctors": [],
            "appointments": [],
            "next_doctor_id": 101,
            "next_appointment_id": 1
        }
    
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Warning: {DATA_FILE} is corrupted. Initializing new system data.")
            return {
                "doctors": [],
                "appointments": [],
                "next_doctor_id": 101,
                "next_appointment_id": 1
            }

def _save_data(data):
    """Saves all system data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Classes ---

class Doctor:
    """Represents a Doctor in the system."""
    def __init__(self, doctor_id, name, specialization, timings):
        self.id = doctor_id
        self.name = name
        self.specialization = specialization
        self.timings = timings # e.g., "Mon-Fri 9AM-5PM"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "timings": self.timings
        }

class Patient:
    """Represents a Patient registering for an appointment."""
    def __init__(self, name, age, disease):
        self.name = name
        self.age = age
        self.disease = disease

    def __str__(self):
        return f"{self.name} (Age: {self.age}, Condition: {self.disease})"

# --- Core Management System ---

class HospitalSystem:
    def __init__(self):
        self.data = _load_data()
        self.doctors = [Doctor(**d) for d in self.data["doctors"]]
        
    def _save_state(self):
        """Prepares and saves the current state to the JSON file."""
        self.data["doctors"] = [d.to_dict() for d in self.doctors]
        _save_data(self.data)
        
    def add_doctor(self, name, specialization, timings):
        """Adds a new doctor to the system."""
        doctor_id = self.data["next_doctor_id"]
        new_doctor = Doctor(doctor_id, name, specialization, timings)
        self.doctors.append(new_doctor)
        self.data["next_doctor_id"] += 1
        self._save_state()
        print(f"✅ Doctor {name} ({specialization}) added with ID: {doctor_id}")

    def register_patient(self):
        """Registers a new patient and returns the Patient object."""
        name = input("Enter patient's name: ").strip()
        while True:
            try:
                age = int(input("Enter patient's age: "))
                if age > 0:
                    break
                else:
                    print("Age must be positive.")
            except ValueError:
                print("Invalid age. Please enter a number.")

        disease = input("Describe the disease/symptoms: ").strip()
        
        # We don't save patients globally, only as part of an appointment
        new_patient = Patient(name, age, disease)
        print(f"✅ Patient {name} registered internally for booking.")
        return new_patient

    def show_doctors(self):
        """Displays all registered doctors and their details."""
        if not self.doctors:
            print("\n⚠️ No doctors are currently registered in the system.")
            return

        print("\n--- 🧑‍⚕️ Available Doctors ---")
        for doc in self.doctors:
            print(f"ID: {doc.id} | Name: {doc.name}")
            print(f"  Specialization: {doc.specialization}")
            print(f"  Availability: {doc.timings}")
            print("-" * 35)

    def book_appointment(self):
        """Allows a patient to book an appointment with a doctor."""
        self.show_doctors()
        if not self.doctors:
            return

        # 1. Select Doctor
        doctor_id = None
        while doctor_id is None:
            try:
                doc_id_input = input("Enter Doctor ID for booking: ").strip()
                if not doc_id_input: return # Allow canceling
                
                doc_id = int(doc_id_input)
                selected_doctor = next((d for d in self.doctors if d.id == doc_id), None)
                
                if selected_doctor:
                    doctor_id = doc_id
                    break
                else:
                    print("❌ Invalid Doctor ID.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
        
        # 2. Register Patient
        print("\n--- Patient Registration ---")
        patient_obj = self.register_patient()
        
        # 3. Book Details
        appointment_id = self.data["next_appointment_id"]
        
        new_appointment = {
            "id": appointment_id,
            "doctor_id": doctor_id,
            "doctor_name": selected_doctor.name,
            "patient": patient_obj.__str__(), # Store patient details as a string
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Scheduled"
        }
        
        self.data["appointments"].append(new_appointment)
        self.data["next_appointment_id"] += 1
        self._save_state()
        
        print(f"\n🎉 Appointment Booked Successfully!")
        print(f"Appointment ID: {appointment_id}")
        print(f"Doctor: Dr. {selected_doctor.name} ({selected_doctor.specialization})")
        print(f"Patient: {patient_obj.name}")

    def show_appointments(self):
        """Displays all scheduled appointments."""
        appointments = self.data["appointments"]
        if not appointments:
            print("\n⚠️ No appointments have been booked yet.")
            return

        print("\n--- 🗓️ Current Appointments ---")
        for app in appointments:
            print(f"ID: {app['id']} | Status: {app['status']}")
            print(f"  Time: {app['time']}")
            print(f"  Doctor: Dr. {app['doctor_name']} (ID: {app['doctor_id']})")
            print(f"  Patient: {app['patient']}")
            print("-" * 35)

# --- Main CLI Application ---

def main():
    """Runs the main command-line interface for the HMS."""
    system = HospitalSystem()
    print("Welcome to the Hospital Management System CLI.")
    
    # Initialize with default doctor if system is empty
    if not system.doctors:
        print("Initializing with some default data...")
        system.add_doctor("Smith", "Cardiology", "Mon, Wed, Fri 10AM-2PM")
        system.add_doctor("Jones", "Pediatrics", "Tue, Thu 9AM-5PM")
    
    while True:
        print("\n*** HMS Main Menu ***")
        print("1. Add New Doctor")
        print("2. Show Doctors")
        print("3. Book Appointment")
        print("4. Show Appointments")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            name = input("Doctor Name: ").strip()
            spec = input("Specialization: ").strip()
            times = input("Available Timings (e.g., Mon-Fri): ").strip()
            if name and spec and times:
                system.add_doctor(name, spec, times)
            else:
                print("❌ All fields are required.")

        elif choice == '2':
            system.show_doctors()

        elif choice == '3':
            system.book_appointment()

        elif choice == '4':
            system.show_appointments()

        elif choice == '5':
            print("Thank you for using the HMS. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
