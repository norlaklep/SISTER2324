import xmlrpc.client
from datetime import datetime

def login():
    user_type = input("Enter user type (admin/patient): ")
    username = input("Enter username: ")
    return user_type, username

def choose_clinic(client):
    clinics = client.get_clinics()
    print("Choose a clinic:")
    for clinic_name, opening_hours in clinics.items():
        print(f"{clinic_name} : {opening_hours}")

    clinic_name = input("Enter the name of the clinic you want to register to: ")
    return clinic_name

def get_patient_info():
    medical_record_number = input("Enter your medical record number (e.g., 12-34-56): ")
    name = input("Enter your name: ")
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    return medical_record_number, name, birthdate

def remove_patient_queue(client, username):
    remove_queue = input("Do you want to remove your existing queue? (yes/no): ")
    if remove_queue.lower() == "yes":
        try:
            response = client.remove_queue(username)
            if response:
                print("Queue removed.")
            else:
                print("Queue not found.")
        except Exception as e:
            print(f"Error removing queue: {e}")

def main():
    client = xmlrpc.client.ServerProxy('http://127.0.0.1:5555/')
    user_type, username = login()

    while True:
        print("\nOptions:")
        print("1. Register to a clinic")
        print("2. Check current queue")
        print("3. Estimate wait time")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            if user_type == "patient":
                clinic_name = choose_clinic(client)

                if not client.is_patient_registered(username):
                    response = client.register(username, clinic_name, *get_patient_info())
                    if response != -1:
                        print(f"Registered successfully. Your queue number is {response}")
                    elif response == -2:
                        print("The chosen clinic is currently closed. Please choose another time or clinic.")
                    else:
                        print("You are already registered.")
                        remove_patient_queue(client, username)
                else:
                    print("You are already registered.")
                    remove_patient_queue(client, username)

            elif user_type == "admin":
                print("Admins cannot register to clinics.")

        elif choice == "2":
            response = client.get_queue()
            print(f"Current queue: {response}")

        elif choice == "3":
            if user_type == "patient":
                client_number = int(input("Enter your queue number: "))
                response = client.estimate_wait_time(client_number)
                if response != -1:
                    print(f"Your estimated wait time is {response} minutes.")
                else:
                    print("Invalid client number.")
            elif user_type == "admin":
                print("
