import socket
import threading

# Dicionário que irá manter informações sobre os clientes conectados.
clientes = {}

# Função para enviar uma mensagem a todos os clientes, exceto o remetente
def broadcast(mensagem, cliente_enviador):
    # Itera por todos os clientes no dicionário "clientes"
    for cliente in clientes:
        # Verifica se o cliente atual não é o mesmo do cliente que enviou a mensagem (cliente_enviador)
        if cliente != cliente_enviador:
            try:
                # Tenta enviar a mensagem usando o socket server_socket_data para o cliente atual
                server_socket_data.sendto(mensagem, cliente)
            except Exception as e:
                # Em caso de exceção durante o envio, imprime uma mensagem de erro no servidor
                print("Ocorreu uma exceção:", e)

# Função para remover um cliente do servidor
def remover(cliente):
    nome = clientes[cliente] # Obtém o nome do cliente com base no endereço
    if cliente in clientes: # Verifica se o cliente está presente no dicionário de clientes
        # Imprime no servidor que o cliente se desconectou
        print(nome + " desconectou-se do servidor.")
        # Envia uma mensagem de desconexão para o cliente que está sendo removido
        server_socket_control.sendto(f"Voce desconectou-se do chat.".encode('utf-8'), cliente)
        # Envia uma mensagem de desconexão para todos os outros clientes
        broadcast(f"{nome} desconectou-se do chat.".encode('utf-8'), cliente)
        del clientes[cliente] # Remove o cliente do dicionário de clientes

# Função para encontrar um cliente pelo nome
def encontrar_cliente_por_nome(destinatario):
    for endereco, nome in clientes.items():
        if nome == destinatario:
            return endereco  # Retorna o endereço do cliente com o nome correspondente
    return False  # Retorna False se o cliente não for encontrado

# Função para lidar com um cliente
def lidar_com_cliente(cliente):
    m_data, m_control, endereco= cliente # Desempacota os elementos da tupla cliente
    nome = clientes[endereco] # Obtém o nome do cliente com base no endereço

    try:
        mensagem_data = m_data.decode('utf-8') # Decodifica a mensagem de dados do cliente
        mensagem_control = m_control.decode('utf-8') # Decodifica a mensagem de controle do cliente

        if mensagem_data.startswith('/MSG'):
            # Se a mensagem de dados começa com '/MSG', é uma mensagem pública
            mensagem_broadcast = f"[{nome}]: {mensagem_data[5:]}" # Formata a mensagem com o nome do remetente
            broadcast(mensagem_broadcast.encode('utf-8'), endereco) # Envia a mensagem a todos os clientes

        elif mensagem_data.startswith('/PRIV'):
            partes = mensagem_data.split(' ')
            destinatario = partes[1] # Obtém o destinatário da mensagem privada
            mensagem_privada = ' '.join(partes[2:]) # Obtém o texto da mensagem privada
            
            destinatario = encontrar_cliente_por_nome(destinatario) # Encontra o endereço do destinatário

            if destinatario:
                # Se o destinatário for encontrado, envia uma mensagem privada
                server_socket_data.sendto(f"[PRIVADO de {nome}]: {mensagem_privada}".encode('utf-8'), destinatario)
            else:
                # Se o destinatário não for encontrado, envia uma mensagem de erro para o remetente
                server_socket_control.sendto("Usuário não encontrado.".encode('utf-8'), endereco)

        elif mensagem_control.startswith('/EXIT'):
            # Se a mensagem de controle começa com '/EXIT', o cliente quer sair
            remover(endereco) # Chama a função para remover o cliente do servidor
        else:
            # Se a mensagem não corresponde a nenhum comando válido, envia uma mensagem de erro ao cliente
            server_socket_control.sendto("Comando inválido.".encode('utf-8'), endereco)
    except Exception as e:
        # Captura exceções que podem ocorrer durante o processamento das mensagens
        print("Ocorreu uma exceção:", e)

def main():
    # Define o host como "0.0.0.0" para permitir conexões de qualquer endereço IP.
    host = "0.0.0.0"
    port_data = 8080
    port_control = 8081

    #Cria dois sockets: server_socket_data para comunicação de dados e server_socket_control para comunicação de controle com os clientes.
    global server_socket_data
    server_socket_data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_data.bind((host, port_data))

    global server_socket_control
    server_socket_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket_control.bind((host, port_control))

    print(f"Servidor de chat está ativo nas portas {port_data} (dados) e {port_control} (controle)")

    while True:
        try:
            # Recebe mensagens de dados e controle dos clientes
            mensagem_data, endereco = server_socket_data.recvfrom(1024)
            mensagem_control, endereco = server_socket_control.recvfrom(1024)

            # Cria uma tupla contendo as mensagens e o endereço do cliente
            cliente_info = (mensagem_data, mensagem_control, endereco)

            # Verifica se o endereço do cliente não está no dicionário de clientes
            if endereco not in clientes:
                # Decodifica a mensagem de dados para obter o nome do cliente
                nick = mensagem_data.decode('utf-8')
                # Adiciona o cliente ao dicionário de clientes com o endereço como chave e o nome como valor
                clientes[endereco] = nick

                print(nick + " conectou-se ao servidor.")
                server_socket_control.sendto("Voce conectou-se ao chat.".encode('utf-8'), endereco)
                broadcast(f"{nick} conectou-se ao chat.".encode('utf-8'), endereco)
            else:
                # A proxima iteração do cliente vai cair aqui
                # Se o cliente já existe no dicionário, chama a função para lidar com as mensagens do cliente
                lidar_com_cliente(cliente_info)
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
