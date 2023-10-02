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
    port_data = 8080    # Porta para mensagens de chat
    port_control = 8081 # Porta para mensagens de controle

    client_socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_data.connect((host, port_data))

    client_socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_control.connect((host, port_control))

    # Registre a entrada no servidor
    nome = input("Digite seu nome: ")
    client_socket_control.send(nome.encode('utf-8'))

    # Inicie threads para receber e enviar mensagens
    # thread_receber_control = threading.Thread(target=receber_mensagens, args=(client_socket_control,))
    # tthread_enviar_control = threading.Thread(target=enviar_mensagem, args=(client_socket_control,))

    thread_receber = threading.Thread(target=receber_mensagens, args=(client_socket_data,))
    thread_enviar = threading.Thread(target=enviar_mensagem, args=(client_socket_data,))
    
    # thread_receber_control.start()
    # tthread_enviar_control.start()

    thread_receber.start()
    thread_enviar.start()

    while True:
        pass

if __name__ == "__main__":
    main()
