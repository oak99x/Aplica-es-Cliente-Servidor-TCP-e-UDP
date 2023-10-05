import socket
import threading

clientes = {}

def broadcast_to_others(mensagem, cliente_enviador):
    for cliente in clientes:
        if cliente != cliente_enviador:
            try:
                server_socket.sendto(mensagem, cliente)
            except:
                print("erro")
                #remover(cliente, conexao)

def lidar_com_cliente(cliente_info, nome):
    data, addr = cliente_info
    mensagem = data.decode('utf-8')

    try:
        if mensagem:
            if mensagem.startswith('/PRIVMSG'):
                partes = mensagem.split(' ')
                destinatario = partes[1]
                mensagem_privada = ' '.join(partes[2:])

                for cliente in clientes.items():
                    if cliente[1] == destinatario:
                        dest = cliente[0]
                        server_socket.sendto(f"[PRIVADO para {destinatario}]: {mensagem_privada}".encode('utf-8'), dest)
                        break
                else:
                    server_socket.sendto("Usuário não encontrado.".encode('utf-8'), addr)
            elif mensagem.startswith('/MSG'):
                mensagem_broadcast = f"[{nome}]: {mensagem[5:]}"
                broadcast_to_others(mensagem_broadcast.encode('utf-8'), addr)
            elif mensagem.startswith('/EXIT'):
                remover(nome, addr)
            else:
                server_socket.sendto("Comando inválido.".encode('utf-8'), addr)
    except:
        remover(nome, addr)

def remover(nome, conexao):
    if nome in clientes.values():
        server_socket.sendto("--X--".encode('utf-8'), conexao)
        del clientes[conexao]
        broadcast_to_others(f"{nome} desconectou-se do servidor".encode('utf-8'), ('0', 8080))

def main():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '0.0.0.0'
    port = 8080
    server_socket.bind((host, port))
    print("--- Server online ---")

    while True:
        data, addr = server_socket.recvfrom(1024)
        cliente_info = (data, addr)

        if addr not in clientes:
            nick = data.decode('utf-8')
            clientes[addr] = nick
            print(f"Usuario {nick} logado.")
            broadcast_to_others(f"{nick} entrou na sala.".encode('utf-8'), addr)
        else:
            nome = clientes[addr]
            lidar_com_cliente(cliente_info, nome)

if __name__ == '__main__':
    main()
