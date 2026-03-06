import paramiko
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.hash_utils import calculate_sha256

HOST = "127.0.0.1"
PORT = 2222

transport = paramiko.Transport((HOST, PORT))
transport.connect()

channel = transport.open_session()

file_path = "../files/sample.txt"
file_name = os.path.basename(file_path)

with open(file_path, "rb") as f:
    file_data = f.read()

local_hash = calculate_sha256(file_path)

channel.send(file_name.encode())
channel.send(file_data)

server_hash = channel.recv(1024).decode()

print("Connected to server securely")
print("Local SHA256 :", local_hash)
print("Server SHA256:", server_hash)

if local_hash == server_hash:
    print("Integrity verified. Secure transfer successful.")
else:
    print("Integrity check failed.")

channel.close()
transport.close()