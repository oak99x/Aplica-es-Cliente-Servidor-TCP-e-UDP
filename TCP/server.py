import socket
import threading

clientes = {}

def broadcast(mensagem, cliente_enviador):
    for cliente, conexoes in clientes.items():
        if cliente != cliente_enviador:
            try:
                conexoes[0].send(mensagem)
            except Exception as e:
                print("Ocorreu uma exceção:", e)
            

def remover(cliente):
    nome = clientes[cliente][2]
    if cliente in clientes:
        print(nome + " desconectou-se do servidor.") #print no servidor
        clientes[cliente][0].send("Voce desconectou-se do chat.".encode('utf-8')) #print para o cliente
        broadcast(f"{nome} desconectou-se do chat.".encode('utf-8'), cliente) #print para todos os clientes

        clientes[cliente][0].close()
        clientes[cliente][1].close()
 
        del clientes[cliente]


def encontrar_cliente_por_nome(destinatario):
    for cliente, info_cliente in clientes.items():
        nome = info_cliente[2]
        if nome == destinatario:
            return info_cliente[0]  # Retorna a conexão com o nome correspondente
    return False  # Retorna False se o cliente não for encontrado

def lidar_com_cliente(cliente):

    conexao_data, conexao_control, endereco = cliente
    nome = clientes[endereco][2]

    while True:
        try:
            mensagem_control = conexao_control.recv(1024).decode('utf-8')
            mensagem_data = conexao_data.recv(1024).decode('utf-8')

            if mensagem_data.startswith('/MSG'):
                mensagem_broadcast = f"[{nome}]: {mensagem_data[5:]}"
                broadcast(mensagem_broadcast.encode('utf-8'), endereco)

            elif mensagem_data.startswith('/PRIV'):
                partes = mensagem_data.split(' ')
                destinatario = partes[1]
                mensagem_privada = ' '.join(partes[2:])
                
                destinatario = encontrar_cliente_por_nome(destinatario)
                
                if destinatario:
                    destinatario.send(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'))
                else:
                    conexao_control.send("Usuário não encontrado.".encode('utf-8'))
            
            elif mensagem_control.startswith('/EXIT'):
                remover(endereco)
                break
                
            else:
                conexao_data.send("Comando inválido.".encode('utf-8'))
        except Exception as e:
            pass

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
        try:
            cliente_data, endereco = server_socket_data.accept()
            cliente_control, endereco = server_socket_control.accept()
            
            cliente_info = (cliente_data, cliente_control, endereco)
            for cliente, info_cliente in clientes.items():
                print(cliente) 
            if endereco not in clientes:
                nick = cliente_data.recv(1024).decode('utf-8')
                cliente_control.recv(1024).decode('utf-8') #limpa o cliente_control

                clientes[endereco] = [cliente_data, cliente_control, nick]

                print(nick + " conectou-se ao servidor.") #print no servidor
                cliente_control.send("Voce conectou-se ao chat.".encode('utf-8')) #print para o cliente
                broadcast(f"{nick} conectou-se ao chat.".encode('utf-8'), endereco) #print para todos os clientes

                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente_info,))
                thread_cliente.start()
            else:
                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente_info,))
                thread_cliente.start()
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
