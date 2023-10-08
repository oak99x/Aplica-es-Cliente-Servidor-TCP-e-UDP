# Laboratório de Redes de Computadores
# Trabalho I - Aplicações Cliente/Servidor TCP e UDP

#### Alunos:
#### Gustavo Geyer Arrussul Winkler dos Santos
#### Mateus de Carvalho de Freitas

## Descrição
Este repositório contém duas aplicações de exemplo de cliente/servidor implementadas usando os protocolos TCP e UDP. As aplicações são projetadas para permitir a comunicação entre um cliente e um servidor em uma rede local.

## Funcionalidades

### Aplicação Cliente/Servidor TCP e UDP
- O cliente pode se conectar a um servidor (TCO ou UDP) na rede.
- Os clientes podem enviar mensagens de chat para o servidor.
- O servidor retransmite as mensagens para os clientes conectados, permitindo uma comunicação de chat em grupo.

## Requisitos
- Python 3.x
- Biblioteca de soquetes (socket) do Python

## Executando as Aplicações
- Execute o servidor correspondente (TCP ou UDP) em uma máquina da rede.
- Execute o cliente correspondente (TCP ou UDP) em outra máquina ou na mesma máquina local para testar a comunicação.

Obs: o host default no cliente está como `localhost`, para executar em outra maquina é necessário verificar o `IP` da maquina que o servidor será executado e editar no cliente.

## Exemplos de Uso
- Execute `python servidor.py` em uma máquina como servidor TCP.
- Execute `python cliente.py` em outra máquina ou na mesma máquina local para se conectar ao servidor TCP.

