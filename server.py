import socket
import threading

clientes = {}

def broadcast(mensagem, cliente_enviador):
    for cliente, conexao in clientes.items():
        if cliente != cliente_enviador:
            try:
                conexao.send(mensagem)
            except:
                remover(cliente, conexao)

def lidar_com_cliente(cliente):
    nome, conexao = cliente
    clientes[nome] = conexao
    print(nome + " conectou-se ao servidor.")
    
    while True:
        try:
            mensagem = conexao.recv(1024)
            if mensagem:
                mensagem = mensagem.decode('utf-8')
                if mensagem.startswith('/PRIVMSG'):
                    partes = mensagem.split(' ')
                    destinatario = partes[1]
                    mensagem_privada = ' '.join(partes[2:])
                    if destinatario in clientes:
                        clientes[destinatario].send(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'))
                    else:
                        conexao.send("Usuário não encontrado.".encode('utf-8'))
                elif mensagem.startswith('/MSG'):
                    mensagem_broadcast = f"[{nome}]: {mensagem[5:]}"
                    broadcast(mensagem_broadcast.encode('utf-8'), conexao)
                else:
                    conexao.send("Comando inválido.".encode('utf-8'))
        except:
            remover(nome, conexao)
            break

def remover(nome, conexao):
    if nome in clientes:
        print(nome + " desconectou-se do servidor.")
        del clientes[nome]
        conexao.close()

def main():
    host = "0.0.0.0"  # Ouça em todas as interfaces disponíveis
    port = 8080       # Porta do servidor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Servidor de chat está ativo na porta " + str(port))

    while True:
        cliente, endereco = server_socket.accept()
        nome = cliente.recv(1024).decode('utf-8')
        cliente_info = (nome, cliente)  # Armazenar o nome e a conexão do cliente
        thread_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente_info,))
        thread_cliente.start()

if __name__ == "__main__":
    main()
