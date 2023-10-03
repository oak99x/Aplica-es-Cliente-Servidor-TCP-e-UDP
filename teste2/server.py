import socket
import threading

clientes = {}

def broadcast(mensagem, cliente):
    for nome, conexoes in clientes.items():
        # if cliente in conexoes:
        #     continue

        try:
            conexoes[0].send(mensagem)
        except:
            pass
            

def remover(nome, cliente):
    if nome in clientes:
        clientes[nome].remove(conexao_data)
        if not clientes[nome]:
            print(nome + " desconectou-se do servidor.")
            broadcast(f"{nome} desconectou-se do chat.".encode('utf-8'), conexao_data)
            del clientes[nome]

def lidar_com_cliente(cliente):

    nome, conexao_data, conexao_control = cliente

    if nome not in clientes:
        clientes[nome] = [conexao_data, conexao_control]
        print(nome + " conectou-se ao servidor.") #print no servidor
        conexao_data.send("Voce conectou-se ao servidor.".encode('utf-8')) #print para o cliente
        broadcast(f"{nome} conectou-se ao chat.".encode('utf-8'), conexao_data) #print para todos os clientes
    else:
        clientes[nome].append(conexao_data)
        clientes[nome].append(conexao_control)

    while True:
        try:
            mensagem_data = conexao_data.recv(1024).decode('utf-8')
            # mensagem_control = conexao_control.recv(1024).decode('utf-8') #arrumar cliente para que fique enviando algo em branco

            if mensagem_data:
                if mensagem_data.startswith('/MSG'):
                    mensagem_broadcast = f"[{nome}]: {mensagem_data[5:]}"
                    broadcast(mensagem_broadcast.encode('utf-8'), conexao_data)

                elif mensagem_data.startswith('/PRIV'):
                    partes = mensagem_data.split(' ')
                    destinatario = partes[1]
                    mensagem_privada = ' '.join(partes[2:])

                    if destinatario in clientes:
                        conexao_destinatario = clientes[destinatario][0]
                        mensagem_privada = f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8')
                        conexao_destinatario.send(mensagem_privada)
                    else:
                        conexao_data.send("Usuário não encontrado.".encode('utf-8'))
                else:
                    conexao_data.send("Comando inválido.".encode('utf-8'))
            
            elif mensagem_control:
                if mensagem_control.startswith('/EXIT'):
                    remover(nome, conexao_control)
                    break  # Sair do loop quando o cliente se desconectar
                else:
                    conexao_data.send("Comando de controle inválido.".encode('utf-8'))
        except:
            remover(nome, conexao_data)
            break

def main():
    host = "0.0.0.0"
    port_data = 8080
    port_control = 8081

    server_socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_data.bind((host, port_data))
    server_socket_data.listen(5)

    server_socket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_control.bind((host, port_control))
    server_socket_control.listen(5)

    print(f"Servidor de chat está ativo nas portas {port_data} (dados) e {port_control} (controle)")

    while True:
        cliente_data, endereco_data = server_socket_data.accept()
        cliente_control, endereco_control = server_socket_control.accept()
        nome = cliente_data.recv(1024).decode('utf-8')
        cliente_info = (nome, cliente_data, cliente_control)

        thread_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente_info,))
        thread_cliente.start()

if __name__ == "__main__":
    main()
