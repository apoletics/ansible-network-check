import socket, sys

UDP_IP = sys.argv[1]
UDP_PORT = sys.argv[2]
FILE  = sys.argv[3]

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, int(UDP_PORT)))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    f = open(FILE, "a")
    f.write(data+"\r\n")
    f.close()
