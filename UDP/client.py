import socket
import threading

def receber_mensagens(client_socket):
    while True:
        mensagem, _ = client_socket.recvfrom(1024)
        mensagem = mensagem.decode('utf-8')
        if not mensagem:
            # Quando o encerramento da aplicação é solicitado, feche as conexões
            client_socket.close()
            break
        print(mensagem)

def enviar_mensagem(client_socket_data, client_socket_control, port_data, port_control, host):
    while True:
        try:
            mensagem = input()
            client_socket_data.sendto(mensagem.encode('utf-8'), (host, port_data))
            client_socket_control.sendto(mensagem.encode('utf-8'), (host, port_control))
        except:
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
    #bug com as threads
    #não ta sendo executado, pois está sendo atropelado pela concorrencia e pula direto para a função enviar_mensagem
    #registrar_nome(client_socket_control, host, port_control)
    print("Digite seu nome: ")

    thread_receber_control = threading.Thread(target=receber_mensagens, args=(client_socket_control,))
    thread_receber_data = threading.Thread(target=receber_mensagens, args=(client_socket_data,))
    
    thread_receber_control.start()
    thread_receber_data.start()

    enviar_mensagem(client_socket_data, client_socket_control, port_data, port_control, host)
    
    thread_receber_control.join()
    thread_receber_data.join()

if __name__ == "__main__":
    main()
