import socket
import threading
import time

class ClinicQueue:
    def __init__(self):
        self.queue = []
        self.current_number = 1

    def enqueue(self, client_name):
        number = self.current_number
        self.queue.append((number, client_name))
        self.current_number += 1
        return number

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def get_queue_data(self):
        return self.queue

    def estimate_wait_time(self, client_number):
        for i, (number, _) in enumerate(self.queue):
            if number == client_number:
                return i * 5  # Assume 5 minutes per patient

        return -1  # Invalid client number

def handle_client(client_socket, clinic_queue):
    client_name = client_socket.recv(1024).decode()
    print(f"Client {client_name} connected.")

    while True:
        data = client_socket.recv(1024).decode()

        if data == "REGISTER":
            number = clinic_queue.enqueue(client_name)
            client_socket.send(f"Registered successfully. Your queue number is {number}".encode())

        elif data == "GET_QUEUE":
            queue_data = clinic_queue.get_queue_data()
            client_socket.send(str(queue_data).encode())

        elif data.startswith("ESTIMATE_WAIT_TIME"):
            _, client_number_str = data.split(" ")
            client_number = int(client_number_str)
            wait_time = clinic_queue.estimate_wait_time(client_number)
            if wait_time != -1:
                client_socket.send(f"Your estimated wait time is {wait_time} minutes.".encode())
            else:
                client_socket.send("Invalid client number.".encode())

        elif data == "EXIT":
            print(f"Client {client_name} disconnected.")
            break

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server listening on port 5555...")

    clinic_queue = ClinicQueue()

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, clinic_queue))
        client_handler.start()

if __name__ == "__main__":
    main()
