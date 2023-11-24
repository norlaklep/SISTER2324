import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    client_name = input("Enter your name: ")
    client.send(client_name.encode())

    while True:
        print("\nOptions:")
        print("1. Register to a clinic")
        print("2. Check current queue")
        print("3. Estimate wait time")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            client.send("REGISTER".encode())
            response = client.recv(1024).decode()
            print(response)

        elif choice == "2":
            client.send("GET_QUEUE".encode())
            response = client.recv(1024).decode()
            print(f"Current queue: {response}")

        elif choice == "3":
            client_number = input("Enter your queue number: ")
            client.send(f"ESTIMATE_WAIT_TIME {client_number}".encode())
            response = client.recv(1024).decode()
            print(response)

        elif choice == "4":
            client.send("EXIT".encode())
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    client.close()

if __name__ == "__main__":
    main()
