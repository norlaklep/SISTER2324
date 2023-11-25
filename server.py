from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import time
from datetime import datetime

class Clinic:
    def __init__(self, name, opening_time, closing_time):
        self.name = name
        self.opening_time = datetime.strptime(opening_time, "%H:%M")
        self.closing_time = datetime.strptime(closing_time, "%H:%M")

class ClinicQueue:
    def __init__(self):
        self.queue = []
        self.current_number = 1
        self.registered_patients = set()
        self.clinics = {
            "Klinik A": Clinic("Klinik A", "08:00", "16:00"),
            "Klinik B": Clinic("Klinik B", "09:00", "12:00"),
            # Tambahkan klinik lainnya di sini
        }

    def enqueue(self, client_name, clinic_name, medical_record_number, birthdate):
        number = self.current_number
        self.queue.append((number, client_name, clinic_name, medical_record_number, birthdate))
        self.current_number += 1
        self.registered_patients.add(client_name)
        return number

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def get_queue_data(self):
        return self.queue

    def estimate_wait_time(self, client_number):
        for i, (number, _, _, _, _) in enumerate(self.queue):
            if number == client_number:
                return i * 5  # Assume 5 minutes per patient

        return -1  # Invalid client number

    def is_patient_registered(self, client_name):
        return client_name in self.registered_patients

    def remove_queue(self, client_name):
        for i, (number, name, _, _, _) in enumerate(self.queue):
            if name == client_name:
                del self.queue[i]
                self.registered_patients.remove(client_name)
                print(f"Queue removed for {client_name}")
                return True

        print(f"Queue not found for {client_name}")
        return False

    def is_clinic_open(self, clinic_name):
        now = datetime.now().time()
        clinic = self.clinics.get(clinic_name)
        if clinic:
            return clinic.opening_time <= now <= clinic.closing_time
        else:
            return False

clinic_queue = ClinicQueue()

def register(client_name, clinic_name, medical_record_number, birthdate):
    if clinic_queue.is_patient_registered(client_name):
        return -1  # Patient is already registered
    elif not clinic_queue.is_clinic_open(clinic_name):
        return -2  # Clinic is closed
    else:
        return clinic_queue.enqueue(client_name, clinic_name, medical_record_number, birthdate)

def get_queue():
    return clinic_queue.get_queue_data()

def estimate_wait_time(client_number):
    return clinic_queue.estimate_wait_time(client_number)

def is_patient_registered(client_name):
    return clinic_queue.is_patient_registered(client_name)

def remove_queue(client_name):
    return clinic_queue.remove_queue(client_name)

def get_clinics():
    clinics_info = {clinic.name: f"{clinic.opening_time.strftime('%H:%M')} - {clinic.closing_time.strftime('%H:%M')}" for clinic in clinic_queue.clinics.values()}
    return clinics_info

def main():
    server = SimpleXMLRPCServer(('127.0.0.1', 5555), requestHandler=SimpleXMLRPCRequestHandler)
    server.register_function(register, 'register')
    server.register_function(get_queue, 'get_queue')
    server.register_function(estimate_wait_time, 'estimate_wait_time')
    server.register_function(is_patient_registered, 'is_patient_registered')
    server.register_function(remove_queue, 'remove_queue')
    server.register_function(get_clinics, 'get_clinics')

    print("Server listening on port 5555...")
    server.serve_forever()

if __name__ == "__main__":
    main()
