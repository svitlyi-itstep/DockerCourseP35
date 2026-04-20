# SERVER
import socket

host = "0.0.0.0"
port = 7000
address = (host, port)

print("Running server...")
server = socket.socket()
server.bind(address)
server.listen()
print(f"Listening to port {port}...")

with open("latest.log", "a+", encoding="utf-8") as file:
    file.write("")

while True:
    client, client_address = server.accept()
    print(f"Connected with {client_address}!")

    response = input("Enter response:")
    client.send(response.encode('utf-8'))
    client.close()

'''

    Змінити сервер так, щоб він не відправляв повідомлення, а отримував.

    Додати логування отриманих повідомлень з вказанням адреси відправника
    та відміткою часу.

    Лог зберігати у файлі.

'''