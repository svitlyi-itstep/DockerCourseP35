# CLIENT
import socket

host = "container-server"
port = 7000
address = (host, port)

server = socket.socket()

print(f"Connecting to server \"{address}\"...")
server.connect(address)

print(f"Connected! Waiting for response...")
response = server.recv(2048).decode('utf-8')

print(f"Response: {response}")

'''
    Зробити json-файл з конфігом, де зберігати адресу сервера
    та порт для підключення.

    Додати можливість ввести повідомлення, яке буде відправлено
    на сервер.

'''