import socket
import paramiko
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.hash_utils import calculate_sha256

HOST = "127.0.0.1"
PORT = 2222

logging.basicConfig(
    filename="../logs/transfer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

host_key = paramiko.RSAKey.generate(2048)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print("Listening for connection...")

client, addr = sock.accept()

transport = paramiko.Transport(client)
transport.add_server_key(host_key)

transport.start_server(server=paramiko.ServerInterface())

channel = transport.accept(20)

if channel is None:
    print("No secure channel established.")
    exit()

print("Secure channel established.")

file_name = channel.recv(1024).decode()

file_data = channel.recv(100000)

save_path = os.path.join("../received", file_name)

with open(save_path, "wb") as f:
    f.write(file_data)

received_hash = calculate_sha256(save_path)

channel.send(received_hash.encode())

logging.info(f"File received: {file_name} | SHA256: {received_hash}")

print("File received securely.")
print("SHA256:", received_hash)

channel.close()
transport.close()
sock.close()