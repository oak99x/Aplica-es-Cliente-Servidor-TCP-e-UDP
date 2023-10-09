import socket
import threading

# Um dicionário que irá manter informações sobre os clientes conectados.
clientes = {}

# Função para enviar uma mensagem a todos os clientes, exceto o remetente
def broadcast(mensagem, cliente_enviador):
    # Itera por todos os clientes no dicionário "clientes"
    for cliente, conexoes in clientes.items():
        # Verifica se o cliente atual não é o mesmo do cliente que enviou a mensagem (cliente_enviador)
        if cliente != cliente_enviador:
            try:
                # Envia a mensagem para o cliente atual (conexoes[0] é o socket de dados do cliente)
                conexoes[0].send(mensagem)
            except Exception as e:
                # Trata qualquer exceção que possa ocorrer durante o envio da mensagem
                print("Ocorreu uma exceção:", e)
            
# Função para remover um cliente do servidor
def remover(cliente):
    # Extrai o nome do cliente do dicionário de clientes
    nome = clientes[cliente][2]
    # Verifica se o cliente existe no dicionário "clientes"
    if cliente in clientes:
        # Imprime uma mensagem no servidor informando que o cliente se desconectou
        print(nome + " desconectou-se do servidor.")
        # Envia uma mensagem para o cliente informando que ele se desconectou (via socket de controle)
        clientes[cliente][0].send("Voce desconectou-se do chat.".encode('utf-8'))
        # Utiliza a função "broadcast" para enviar uma mensagem para todos os outros clientes
        # informando que este cliente se desconectou (excluindo o cliente que está sendo removido)
        broadcast(f"{nome} desconectou-se do chat.".encode('utf-8'), cliente)

        # Fecha os sockets de dados e controle do cliente
        clientes[cliente][0].close()
        clientes[cliente][1].close()

        # Remove o cliente do dicionário de clientes
        del clientes[cliente]

# Função para encontrar um cliente pelo nome
def encontrar_cliente_por_nome(destinatario):
    for cliente, info_cliente in clientes.items():
        # Obtém o nome do cliente atual do dicionário
        nome = info_cliente[2]
        # Verifica se o nome do cliente atual corresponde ao destinatário desejado
        if nome == destinatario:
            # Retorna a conexão (socket de dados) com o nome correspondente
            return info_cliente[0]
    return False  # Retorna False se o cliente não for encontrado

def lidar_com_cliente(cliente):

    conexao_data, conexao_control, endereco = cliente
    nome = clientes[endereco][2]

    while True:
        try:
            # Recebe a mensagem de controle e dados do cliente
            mensagem_control = conexao_control.recv(1024).decode('utf-8')
            mensagem_data = conexao_data.recv(1024).decode('utf-8')

            # Verifica se a mensagem de dados começa com '/MSG', indicando uma mensagem de broadcast
            if mensagem_data.startswith('/MSG'):
                mensagem_broadcast = f"[{nome}]: {mensagem_data[5:]}"
                # Utiliza a função "broadcast" para enviar a mensagem broadcast a todos os clientes
                broadcast(mensagem_broadcast.encode('utf-8'), endereco)

            # Verifica se a mensagem de dados começa com '/PRIV', indicando uma mensagem privada
            elif mensagem_data.startswith('/PRIV'):
                partes = mensagem_data.split(' ')
                destinatario = partes[1]
                mensagem_privada = ' '.join(partes[2:])
                
                # Encontra o cliente de destino pelo nome
                destinatario = encontrar_cliente_por_nome(destinatario)
                
                if destinatario:
                    # Envia a mensagem privada ao destinatário
                    destinatario.send(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'))
                else:
                    # Se o destinatário não for encontrado, envia uma mensagem de erro ao cliente
                    conexao_control.send("Usuário não encontrado.".encode('utf-8'))
            elif mensagem_control.startswith('/LIST'):
                # Se a mensagem comeca com '/LIST', exibe uma lista de usuarios conectados na sala
                lista = "Usuários conectados:\n"
                for cliente, cliente_info in clientes.items():
                    lista += f"{cliente_info[2]} \n"
                lista += "--------"
                conexao_control.send(lista.encode('utf-8'))
                
            elif mensagem_control.startswith('/EXIT'):
                # Chama a função "remover" para desconectar o cliente e encerra o loop
                remover(endereco)
                break    
            else:
                # Se a mensagem não corresponder a nenhum comando conhecido, envia uma mensagem de comando inválido ao cliente
                conexao_data.send("Comando inválido.".encode('utf-8'))
        except Exception as e:
            pass

def main():
    # Define o host como "0.0.0.0" para permitir conexões de qualquer endereço IP.
    host = "0.0.0.0"
    port_data = 8080
    port_control = 8081

    #Cria dois sockets: server_socket_data para comunicação de dados e server_socket_control para comunicação de controle com os clientes.
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
            
            # Quando um cliente se conecta, recebe seu nome, cria uma nova thread para lidar com esse cliente e o adiciona ao dicionário clientes.
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
                # Se o cliente já existe no dicionário, inicia uma nova thread para lidar com esse cliente.
                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(cliente_info,))
                thread_cliente.start()
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
