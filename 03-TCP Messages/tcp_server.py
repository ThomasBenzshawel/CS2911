import socket
from socket import *
import struct
import time
import sys

# Port number definitions
# (May have to be adjusted if they collide with ports in use by other programs/services.)
TCP_PORT = 12100

# Address to listen on when acting as server.
# The address '' means accept any connection for our 'receive' port from any network interface
# on this system (including 'localhost' loopback connection).
LISTEN_ON_INTERFACE = '192.168.1.187'
HOST = 'localhost'

def tcp_receive(listen_on, listen_port):
    """
    - Listen for a TCP connection on a designated "listening" port
    - Accept the connection, creating a connection socket
    - Print the address and port of the sender
    - Repeat until a zero-length message is received:
      - Receive a message, saving it to a text-file (1.txt for first file, 2.txt for second file, etc.)
      - Send a single-character response 'A' to indicate that the upload was accepted.
    - Send a 'Q' to indicate a zero-length message was received.
    - Close data connection.

    :param int listen_port: Port number on the server to listen on
    """
    print('tcp_receive (server): listen_port={0}'.format(listen_port))
    address = (listen_on, listen_port)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)

    s.listen(5)

    c, address = s.accept()
    listen = True
    while listen:
        print('Connected with', address, 'through socket', c.getsockname())
        data = get_n_bytes(c, 4)
        length = int.from_bytes(data, 'big', signed=True)

        f = open("output.txt", "a")

        if length > 0:
            i = 0
            final_string = ""
            rtrn_string = ""
            c.send('A'.encode())
            while i < length:
                decode_bytes = c.recv(1)
                current_char = str(decode_bytes, 'UTF-8')
                if current_char == "\n":
                    rtrn_string += current_char
                    i += 1
                else:
                    rtrn_string += current_char
            final_string += rtrn_string
            print(final_string)
            f.write(final_string)
            f.close()
        else:
            print("closing connection")
            c.send('Q'.encode())
            listen = False
            s.close()



def get_n_bytes(com, n):
    data = b''
    while len(data) < n:
        data += com.recv(1)
    return data


if __name__ == '__main__':
    tcp_receive(LISTEN_ON_INTERFACE, TCP_PORT)
