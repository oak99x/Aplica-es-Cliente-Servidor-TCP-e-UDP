import socket
import threading

def receber_mensagens(client_socket):
    while True:
        mensagem = client_socket.recv(1024).decode('utf-8')
        print(mensagem)

def enviar_mensagem(client_socket):
    while True:
        mensagem = input()
        client_socket.send(mensagem.encode('utf-8'))

def main():
    host = 'localhost'  # Endereço do servidor
    port = 8080       # Porta do servidor

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    nome = input("Digite seu nome: ")
    client_socket.send(nome.encode('utf-8'))

    thread_receber = threading.Thread(target=receber_mensagens, args=(client_socket,))
    thread_enviar = threading.Thread(target=enviar_mensagem, args=(client_socket,))

    thread_receber.start()
    thread_enviar.start()

if __name__ == "__main__":
    main()
