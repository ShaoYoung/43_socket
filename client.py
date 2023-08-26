import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
# создание сокета
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# подключение к серверу
client.connect(('127.0.0.1', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            # получаем сообщение от сервера
            message = client.recv(1024).decode('ascii')
            # если сервер отправил 'NICK'
            if message == 'NICK':
                # отправляем ему nickname
                client.send(nickname.encode('ascii'))
            else:
                # иначе печатаем полученное сообщение
                print(message)
        except:
            # Close Connection When Error
            # если возникло исключение (не смог отправить сообщение серверу)
            print("An error occured!")
            # закрываем соединение
            client.close()
            break

def write():
    while True:
        # формируем текстовое сообщение в формате nickname : сообщение
        message = '{}: {}'.format(nickname, input(''))
        # отправляем сообщение
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
# создаём один поток на приём
receive_thread = threading.Thread(target=receive)
# запускаем его
receive_thread.start()

# создаём второй поток на отправку
write_thread = threading.Thread(target=write)
# запускаем его
write_thread.start()