import socket

clientes = {}

def broadcast_to_others(mensagem, cliente_enviador):
    for cliente, conexao in clientes.items():
        if cliente != cliente_enviador:
            try:
                conexao.sendto(mensagem, ('255.255.255.255', 8080))
            except:
                remover(cliente_enviador, conexao)

def lidar_com_cliente(cliente):
    nome, conexao = cliente
    clientes[nome] = conexao
    print(nome + " conectou-se ao servidor.")
    conexao.sendto(f"{nome} conectou-se do servidor.".encode('utf-8'), ('255.255.255.255', 8080))
    
    while True:
        try:
            mensagem, sender = conexao.recvfrom(1024)
            if mensagem:
                mensagem = mensagem.decode('utf-8')
                if mensagem.startswith('/PRIVMSG'):
                    partes = mensagem.split(' ')
                    destinatario = partes[1]
                    mensagem_privada = ' '.join(partes[2:]) ## PROCURAR COM DICT
                    if destinatario in clientes:
                        dest = clientes[destinatario][0]
                        dest.sendto(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'), (dest[1]))
                    else:
                        conexao.sendto("Usuário não encontrado.".encode('utf-8'), sender)
                elif mensagem.startswith('/MSG'):
                    mensagem_broadcast = f"[{sender}]: {mensagem[5:]}"
                    broadcast_to_others(mensagem_broadcast.encode('utf-8'), sender)
                elif mensagem.startswith('/EXIT'):
                    remover(sender, conexao)
                else:
                    conexao.send("Comando inválido.".encode('utf-8'))
        except:
            remover(sender, conexao)
            break

def remover(nome, conexao):
    if nome in clientes:
        print(nome[0] + " desconectou-se do servidor.")
        del clientes[nome]
        conexao.sendto("{nome} desconectou-se do servidor.".encode('utf-8'), ('255.255.255.255', 8080))
        conexao.close()

def main():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '0.0.0.0'
    port = 8080
    # bind to the port
    server_socket.bind((host, port))
    print("Server started")

    while True:
        # receive data from the client
        data, addr = server_socket.recvfrom(1024)
        print("received message: %s" % data.decode('utf-8'))

        # send data to the client
        server_socket.sendto(data, addr)

if __name__ == '__main__':
    main()
