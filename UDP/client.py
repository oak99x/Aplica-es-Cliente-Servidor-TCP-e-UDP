import socket
import threading
import time

# Função para receber mensagens do servidor
# recebe mensagens do servidor e as imprime na tela do cliente.
def receber_mensagens(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            mensagem, _ = client_socket.recvfrom(1024)
            mensagem = mensagem.decode('utf-8')
            print(mensagem)
        except Exception as e:
            pass

# Função para enviar mensagens para o servidor
# permite ao  cliente enviar mensagens para o servidor e também para o controle. 
# Ela verifica se o cliente digitou "/exit" para encerrar a conexão.
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

# Função para registrar o nome do cliente no servidor (não está sendo usada atualmente)
def registrar_nome(client_socket, host, port_control):
    nome = input("Digite seu nome: ")
    client_socket.sendto(nome.encode('utf-8'), (host, port_control))

def main():
    #Define o host (endereço do servidor) e as portas para mensagens de chat (port_data) e mensagens de controle (port_control).
    host = 'localhost'  # Endereço do servidor
    port_data = 8080    # Porta para mensagens de chat
    port_control = 8081 # Porta para mensagens de controle

    # Cria dois sockets: client_socket_data para comunicação de dados e client_socket_control para comunicação de controle com o servidor.
    global client_socket_data
    global client_socket_control

    client_socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Registre a entrada no servidor
    # registrar_nome(client_socket_control, host, port_control)
    print("Digite seu nome: ")

    stop_event = threading.Event()  # Evento para sinalizar o encerramento

    # Inicia duas threads para receber mensagens do servidor: uma para mensagens de controle e outra para mensagens de dados.
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
