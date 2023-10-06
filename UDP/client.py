import socket
import threading
import time

def receber_mensagens(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            mensagem, _ = client_socket.recvfrom(1024)
            mensagem = mensagem.decode('utf-8')
            print(mensagem)
        except Exception as e:
            pass

def enviar_mensagem(client_socket_data, client_socket_control, port_data, port_control, host, stop_event):
    while not stop_event.is_set():
        try:
            mensagem = input()
            client_socket_data.sendto(mensagem.encode('utf-8'), (host, port_data))
            client_socket_control.sendto(mensagem.encode('utf-8'), (host, port_control))
            if mensagem.lower() == '/exit':
                stop_event.set()  # Sinalize para sair
        except Exception as e:
            break

def registrar_nome(client_socket, host, port_control):
    nome = input("Digite seu nome: ")
    client_socket.sendto(nome.encode('utf-8'), (host, port_control))

def main():
    host = 'localhost'  # Endereço do servidor
    port_data = 8080    # Porta para mensagens de chat
    port_control = 8081 # Porta para mensagens de controle

    global client_socket_data
    global client_socket_control

    client_socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Registre a entrada no servidor
    # registrar_nome(client_socket_control, host, port_control)
    print("Digite seu nome: ")

    stop_event = threading.Event()  # Evento para sinalizar o encerramento

    thread_receber_control = threading.Thread(target=receber_mensagens, args=(client_socket_control, stop_event))
    thread_receber_data = threading.Thread(target=receber_mensagens, args=(client_socket_data, stop_event))
    
    thread_receber_control.start()
    thread_receber_data.start()

    enviar_mensagem(client_socket_data, client_socket_control, port_data, port_control, host, stop_event)

    # Aguarde até que a thread de envio sinalize o encerramento
    stop_event.wait()

    # Feche os sockets
    client_socket_control.close()
    client_socket_data.close()

if __name__ == "__main__":
    main()
