#!/bin/python3
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
# создание сокета
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# связка сокета с хостом и портом
server.bind((host, port))
# запуск сокета в режиме прослушивания. аргументом можно передать максимальное количество подключения в очереди
server.listen()

# Lists For Clients and Their Nicknames
# глобальные переменные
# клиенты (их сокеты)
clients = []
# имена клиентов
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    # для каждого client из clients
    for client in clients:
        # отправляем сообщение message
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            # получаем данные от клиента (порциями по 1024 байта)
            message = client.recv(1024)
            # вызываем функцию рассылки полученного сообщения всем клиентам из списка clients
            broadcast(message)
        except:
            # Removing And Closing Clients
            # если возникло исключение (неудачная отправка сообщения клиенту)

            # получаем индекс клиента
            index = clients.index(client)
            # удаляем этого клиента из списка clients
            clients.remove(client)

            # закрываем соединение с клиентом
            client.close()
            # получаем имя клиента
            nickname = nicknames[index]
            # оповещаем оставшихся clients о том, что клиент вышел
            broadcast('{} left!'.format(nickname).encode('ascii'))
            # удаляем имя клиента из списка nicknames
            nicknames.remove(nickname)
            # прерываем цикл, завершаем работу функции handle, останавливаем поток
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        # ожидание входящего соединения
        # приём подключения. возвращает кортеж: новый сокет и адрес клиента. используется для приёма и передачи данных клиенту
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        # отправка клиенту 'NICK' в кодировке 'ascii'
        client.send('NICK'.encode('ascii'))
        # приём данных (порциями по 1024 байта) от клиента, декодирование и сохранение в переменной nickname
        nickname = client.recv(1024).decode('ascii')

        # добавляем имя клиента в список
        nicknames.append(nickname)
        # добавляем сокет клиента в список
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        # вызов функции broadcast. аргумент - сообщение
        broadcast("{} joined!".format(nickname).encode('ascii'))
        # отправка клиенту сообщения о подключении к серверу
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        # для каждого клиента запускаем обработчик в отдельном потоке
        thread = threading.Thread(target=handle, args=(client,))
        # стартуем поток
        thread.start()

print("Server if listening...")
receive()
