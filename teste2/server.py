import socket
import threading

clientes = {}
mensagens = []

def broadcast(mensagem, cliente):
    for nome, conexao in clientes.items():
        if nome == cliente: #****** !=
            try:
                conexao.send(mensagem)
            except:
                remover(nome, conexao)

def remover(nome, conexao):
    if nome in clientes:
        print(nome + " desconectou-se do servidor.") # print no servidor
        broadcast(f"{nome} saiu do chat.".encode('utf-8'), nome) # print para todos clientes
        del clientes[nome]
        conexao.close()

def lidar_com_cliente(cliente, controle):
    nome, conexao = cliente
    clientes[nome] = conexao
    print(nome + " conectou-se ao servidor.") # print servidor
    broadcast(f"{nome} conectou-se ao servidor.".encode('utf-8'), nome) # print para todos clientes

    while True:
        try:
            if controle:
                mensagem = conexao.recv(1024).decode('utf-8')
                if mensagem:
                    if mensagem.startswith('/EXIT'):
                        nome_cliente = mensagem.split()[1]
                        # print(f"{nome_cliente} saiu do chat.")
                        # broadcast(f"{nome_cliente} saiu do chat.".encode('utf-8'), conexao)
                        remover(nome_cliente, conexao)
                    else:
                        conexao.send("Comando de controle inválido.".encode('utf-8'))
            else:
                mensagem = conexao.recv(1024).decode('utf-8')
                if mensagem:
                    if mensagem.startswith('/MSG'):
                        mensagem_broadcast = f"[{nome}]: {mensagem[5:]}".encode('utf-8')
                        mensagens.append(mensagem_broadcast)
                        broadcast(mensagem_broadcast, conexao)
                    
                    else:
                        conexao.send("Comando inválido.".encode('utf-8'))
        except:
            remover(nome, conexao)
            break



# Para manter controle e ordenação das mensagens no TCP
# def enviar_mensagens(cliente):
#     nome, conexao = cliente.accept()
#     while True:
#         if mensagens:
#             mensagem = mensagens.pop(0)
#             broadcast(mensagem, conexao)

def main():
    host = "0.0.0.0"  # Ouça em todas as interfaces disponíveis
    port_data = 8080  # Porta para mensagens de chat
    port_control = 8081  # Porta para mensagens de controle

    server_socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_data.bind((host, port_data))
    server_socket_data.listen(5)

    server_socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_control.bind((host, port_control))
    server_socket_control.listen(5)

    print(f"Servidor de chat está ativo nas portas {port_data} (dados) e {port_control} (controle)")

    # Para manter controle e ordenação das mensagens no TCP
    # Inicie a thread para enviar mensagens para clientes
    # thread_enviar = threading.Thread(target=enviar_mensagens, args=(server_socket_data,))
    # thread_enviar.start()

    while True:
        cliente_data, endereco_data = server_socket_data.accept()
        nome = cliente_data.recv(1024).decode('utf-8')
        #cliente_info = (endereco[0], cliente)  # Armazenar o ip e a conexão do cliente
        cliente_info = (nome, cliente_data)  # Armazenar o nome e a conexão do cliente
        thread_cliente_data = threading.Thread(target=lidar_com_cliente, args=(cliente_info, False))
        thread_cliente_data.start()

        # Lidar com as mensagens de controle em uma thread separada
        cliente_control, endereco_control = server_socket_control.accept()
        controle_info = (nome, cliente_control)
        thread_cliente_control = threading.Thread(target=lidar_com_cliente, args=(controle_info, True))
        thread_cliente_control.start()

if __name__ == "__main__":
    main()
