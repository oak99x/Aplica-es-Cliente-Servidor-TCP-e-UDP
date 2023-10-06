import socket
import threading

clientes = {}

def broadcast(mensagem, cliente_enviador):
    for cliente in clientes:
        if cliente != cliente_enviador:
            try:
                server_socket_data.sendto(mensagem, cliente)
            except Exception as e:
                print("Ocorreu uma exceção:", e)

def remover(cliente):
    nome = clientes[cliente]
    if cliente in clientes:
        print(nome + " desconectou-se do servidor.")
        server_socket_control.sendto(f"Voce desconectou-se do chat.".encode('utf-8'), cliente)
        broadcast(f"{nome} desconectou-se do chat.".encode('utf-8'), cliente)
        del clientes[cliente]

def encontrar_cliente_por_nome(destinatario):
    for endereco, nome in clientes.items():
        if nome == destinatario:
            return endereco  # Retorna o endereço do cliente com o nome correspondente
    return False  # Retorna None se o cliente não for encontrado

def lidar_com_cliente(cliente):
    m_data, m_control, endereco= cliente
    nome = clientes[endereco]

    try:
        mensagem_data = m_data.decode('utf-8')
        mensagem_control = m_control.decode('utf-8')

        if mensagem_data.startswith('/MSG'):
            mensagem_broadcast = f"[{nome}]: {mensagem_data[5:]}"
            broadcast(mensagem_broadcast.encode('utf-8'), endereco)

        elif mensagem_data.startswith('/PRIV'):
            partes = mensagem_data.split(' ')
            destinatario = partes[1]
            mensagem_privada = ' '.join(partes[2:])
            
            destinatario = encontrar_cliente_por_nome(destinatario)

            if destinatario:
                server_socket_data.sendto(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'), destinatario)
            else:
                server_socket_control.sendto("Usuário não encontrado.".encode('utf-8'), endereco)

        elif mensagem_control.startswith('/EXIT'):
            remover(endereco)
        else:
            server_socket_control.sendto("Comando inválido.".encode('utf-8'), endereco)
    except Exception as e:
        print("Ocorreu uma exceção:", e)

def main():
    host = "0.0.0.0"
    port_data = 8080
    port_control = 8081

    global server_socket_data
    server_socket_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_data.bind((host, port_data))

    global server_socket_control
    server_socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_control.bind((host, port_control))

    print(f"Servidor de chat está ativo nas portas {port_data} (dados) e {port_control} (controle)")

    while True:
        mensagem_data, endereco = server_socket_data.recvfrom(1024)
        mensagem_control, endereco = server_socket_control.recvfrom(1024)

        cliente_info = (mensagem_data, mensagem_control, endereco)

        if endereco not in clientes:
            nick = mensagem_data.decode('utf-8')
            clientes[endereco] = nick

            print(nick + " conectou-se ao servidor.")
            server_socket_control.sendto("Voce conectou-se ao chat.".encode('utf-8'), endereco)
            broadcast(f"{nick} conectou-se ao chat.".encode('utf-8'), endereco)
        else:
            lidar_com_cliente(cliente_info)

if __name__ == "__main__":
    main()
