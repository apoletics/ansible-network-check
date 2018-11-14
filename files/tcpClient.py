import socket, sys

TCP_IP = sys.argv[1]
TCP_PORT = sys.argv[2]
MESSAGE = sys.argv[3]

print MESSAGE
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((TCP_IP, int(TCP_PORT) ))

client.send(MESSAGE)

response = client.recv(4096)

print response
