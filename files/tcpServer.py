import socket, sys, threading

TCP_IP = sys.argv[1]
TCP_PORT = sys.argv[2]
FILE  = sys.argv[3]


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((TCP_IP, int(TCP_PORT)))
            
server.listen(5)

#f = open(FILE, "a")
#f.write("STARTED")
#f.close()


def handle_client(client_socket):
    
    request = client_socket.recv(1024)
    f = open(FILE, "a")
    f.write(request+"\r\n")
    f.close()
    
    client_socket.send(request)
    client_socket.close()
    
while True:
    client, addr = server.accept()    
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
