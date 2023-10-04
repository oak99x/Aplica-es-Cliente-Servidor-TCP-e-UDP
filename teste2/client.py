import socket
import threading

def receber_mensagens(client_socket):
    while True:
        mensagem = client_socket.recv(1024).decode('utf-8')
        if not mensagem:
            # Quando o encerramento da aplicação é solicitado, feche as conexões
            client_socket.close()
            break
        print(mensagem)

def enviar_mensagem(client_socket_data, client_socket_control):
    while True:
        try:
            mensagem = input()
            client_socket_data.send(mensagem.encode('utf-8'))
            client_socket_control.send(mensagem.encode('utf-8'))
        except:
            break
        
def registrar_nome(client_socket_control):
        nome = input("Digite seu nome: ")
        client_socket_control.send(nome.encode('utf-8'))

def main():
    host = 'localhost'  # Endereço do servidor
    port_data = 8080    # Porta para mensagens de chat
    port_control = 8081 # Porta para mensagens de controle

    client_socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_data.connect((host, port_data))

    client_socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket_control.connect((host, port_control))

    # Registre a entrada no servidor
    #bug com as threads
    #não ta sendo executado, pois está sendo atropelado pela concorrencia e pula direto para a função enviar_mensagem
    #registrar_nome(client_socket_control)
    print("Digite seu nome: ")

    # Inicie threads para receber e enviar mensagens
    thread_receber_control = threading.Thread(target=receber_mensagens, args=(client_socket_control,))
    thread_receber = threading.Thread(target=receber_mensagens, args=(client_socket_data,))
    
    thread_receber_control.start()
    thread_receber.start()

    enviar_mensagem(client_socket_data, client_socket_control)
    
    # Quando o envio de mensagens é encerrado, espere que as threads de recebimento terminem
    thread_receber_control.join()
    thread_receber.join()

if __name__ == "__main__":
    main()
