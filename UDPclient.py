import socket
import threading

host = '192.168.68.107'
port = 8080


def receber_mensagens(client_socket):
    while True:
        message = client_socket.recvfrom(1024)[0].decode('utf-8')
        print(message)

def enviar_mensagem(client_socket):

    while True:
        message = input()
        client_socket.sendto(message.encode('utf-8'), (host, port))

def main():
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # get local machine name

    nome = input("Digite seu nick: ")
    client_socket.sendto(nome.encode('utf-8'), (host, port))

    message = input(" -> ")

    thread_receber = threading.Thread(target=receber_mensagens, args=(client_socket,))
    thread_enviar = threading.Thread(target=enviar_mensagem, args=(client_socket,))

    thread_receber.start()
    thread_enviar.start()

if __name__ == '__main__':
    main()
