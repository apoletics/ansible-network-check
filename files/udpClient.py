import socket, sys

UDP_IP = sys.argv[1]
UDP_PORT = sys.argv[2]

MESSAGE = sys.argv[3]

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, int(UDP_PORT)))

