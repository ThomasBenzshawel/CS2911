import random
import sys
import math
from socket import *

# Use these named constants as you write your code
MAX_PRIME = 0b11111111  # The maximum value a prime number can have
MIN_PRIME = 0b11000001  # The minimum value a prime number can have
PUBLIC_EXPONENT = 17  # The default public exponent
TCP_PORT = 12100


# Address of the 'other' ('server') host that should be connected to for 'send' operations.
# When connecting on one system, use 'localhost'
# When 'sending' to another system, use its IP address (or DNS name if it has one)
# OTHER_HOST = '155.92.x.x'


def main():
    """Provide the user with a variety of encryption-related actions"""
    run = True
    while (run):
        # Get chosen operation from the user.
        action = input(
            "Select an option from the menu below:\n"
            "(1-CK) create_keys\n"
            "(2-CC) compute_checksum\n"
            "(3-VC) verify_checksum\n"
            "(4-EM) encrypt_message\n"
            "(5-DM) decrypt_message\n"
            "(6-BK) break_key\n"
            "(7) to send a message to another user\n"
            "(8) to receive a message to another user\n"
            "(9) to end the program\n"
            "Please enter the option you want:\n"
        )
        # Execute the chosen operation.
        if action in ["1", "CK", "ck", "create_keys"]:
            create_keys_interactive()
        elif action in ["2", "CC", "cc", "compute_checksum"]:
            compute_checksum_interactive()
        elif action in ["3", "VC", "vc", "verify_checksum"]:
            verify_checksum_interactive()
        elif action in ["4", "EM", "em", "encrypt_message"]:
            encrypt_message_interactive()
        elif action in ["5", "DM", "dm", "decrypt_message"]:
            decrypt_message_interactive()
        elif action in ["6", "BK", "bk", "break_key"]:
            break_key_interactive()
        elif action in ["7"]:
            send_message()
        elif action in ["8"]:
            recv_message()
        elif action in ["9"]:
            run = False
        else:
            print("Unknown action: '{0}'".format(action))


def get_public_key(key_pair):
    """
    Pulls the public key out of the tuple structure created by
    create_keys()
    :param key_pair: (e,d,n)
    :return: (e,n)
    """

    return (key_pair[0], key_pair[2])


def get_private_key(key_pair):
    """
    Pulls the private key out of the tuple structure created by
    create_keys()
    :param key_pair: (e,d,n)
    :return: (d,n)
    """

    return (key_pair[1], key_pair[2])


def create_keys_interactive():
    """
    Create new public keys
    :return: the private key (d, n) for use by other interactive methods
    """

    key_pair = create_keys()
    pub = get_public_key(key_pair)
    priv = get_private_key(key_pair)
    print("Public key: ")
    print(pub)
    print("Private key: ")
    print(priv)
    return priv


def compute_checksum_interactive():
    """
    Compute the checksum for a message, and encrypt it
    """

    priv = create_keys_interactive()
    message = input("Please enter the message to be checksummed: ")
    hash = compute_checksum(message)
    print("Hash:", "{0:04x}".format(hash))
    cipher = apply_key(priv, hash)
    print("Encrypted Hash:", "{0:04x}".format(cipher))


def verify_checksum_interactive():
    """
    Verify a message with its checksum, interactively
    """

    pub = enter_public_key_interactive()
    message = input("Please enter the message to be verified: ")
    recomputed_hash = compute_checksum(message)

    string_hash = input("Please enter the encrypted hash (in hexadecimal): ")
    encrypted_hash = int(string_hash, 16)
    decrypted_hash = apply_key(pub, encrypted_hash)
    print("Recomputed hash:", "{0:04x}".format(recomputed_hash))
    print("Decrypted hash: ", "{0:04x}".format(decrypted_hash))
    if recomputed_hash == decrypted_hash:
        print("Hashes match -- message is verified")
    else:
        print("Hashes do not match -- has tampering occured?")


def encrypt_message_interactive():
    """
    Encrypt a message
    """

    message = input("Please enter the message to be encrypted: ")
    pub = enter_public_key_interactive()
    encrypted = ""
    for c in message:
        encrypted += "{0:04x}".format(apply_key(pub, ord(c)))
    print("Encrypted message:", encrypted)


def decrypt_message_interactive(priv=None):
    """
    Decrypt a message
    """

    encrypted = input("Please enter the message to be decrypted: ")
    if priv is None:
        priv = enter_key_interactive("private")
    message = ""
    for i in range(0, len(encrypted), 4):
        enc_string = encrypted[i: i + 4]
        enc = int(enc_string, 16)
        dec = apply_key(priv, enc)
        if dec >= 0 and dec < 256:
            message += chr(dec)
        else:
            print("Warning: Could not decode encrypted entity: " + enc_string)
            print("         decrypted as: " + str(dec) + " which is out of range.")
            print("         inserting _ at position of this character")
            message += "_"
    print("Decrypted message:", message)


def break_key_interactive():
    """
    Break key, interactively
    """

    pub = enter_public_key_interactive()
    priv = break_key(pub)
    print("Private key:")
    print(priv)
    decrypt_message_interactive(priv)


def enter_public_key_interactive():
    """
    Prompt user to enter the public modulus.
    :return: the tuple (e,n)
    """

    print("(Using public exponent = " + str(PUBLIC_EXPONENT) + ")")
    string_modulus = input("Please enter the modulus (decimal): ")
    modulus = int(string_modulus)
    return (PUBLIC_EXPONENT, modulus)


def enter_key_interactive(key_type):
    """
    Prompt user to enter the exponent and modulus of a key
    :param key_type: either the string 'public' or 'private' -- used to prompt the user on how
                     this key is interpretted by the program.
    :return: the tuple (e,n)
    """
    string_exponent = input("Please enter the " + key_type + " exponent (decimal): ")
    exponent = int(string_exponent)
    string_modulus = input("Please enter the modulus (decimal): ")
    modulus = int(string_modulus)
    return (exponent, modulus)


def compute_checksum(string):
    """
    Compute simple hash
    Given a string, compute a simple hash as the sum of characters
    in the string.
    (If the sum goes over sixteen bits, the numbers should "wrap around"
    back into a sixteen bit number.  e.g. 0x3E6A7 should "wrap around" to
    0xE6A7)
    This checksum is similar to the internet checksum used in UDP and TCP
    packets, but it is a two's complement sum rather than a one's
    complement sum.
    :param str string: The string to hash
    :return: the checksum as an integer
    """

    total = 0
    for c in string:
        total += ord(c)
    total %= 0x8000  # Guarantees checksum is only 4 hex digits
    # How many bytes is that?
    #
    # Also guarantees that the checksum will
    # always be less than the modulus.
    return total


# ---------------------------------------
# Do not modify code above this line
# ---------------------------------------

# Remember to use the named constants as you write your code
# MAX_PRIME = 0b11111111  The maximum value a prime number can have
# MIN_PRIME = 0b11000001  The minimum value a prime number can have
# PUBLIC_EXPONENT = 17  The default public exponent

def generate_primes(l, h):
    assert l >= 1
    assert h > l
    primes = []
    for x in range(l, h + 1):
        prime = True
        for y in range(2, x):
            if x % y == 0:
                prime = False
                break
        if prime:
            primes.append(x)
    return primes


def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p


x, y = 0, 1


def gcdExtended(a, b):
    global x, y

    # Base Case
    if (a == 0):
        x = 0
        y = 1
        return b
    # To store results of recursive call
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd


def find_e(co_prime):
    i = 2
    while i < co_prime:
        if gcd(i, co_prime) == 1:
            return i
        i += 1
    return -1


def modInverse(A, M):
    g = gcdExtended(A, M)

    return (x % M + M) % M


def create_keys():
    """
    Create the public and private keys.
    :return: the keys as a three-tuple: (e,d,n)
    """
    possibleKeys = generate_primes(1, 255)
    length = possibleKeys.__len__()
    first_key = possibleKeys[random.randint(0, length - 1)]
    second_key = possibleKeys[random.randint(0, length - 1)]

    co_prime = math.lcm(first_key - 1, second_key - 1)
    n = first_key * second_key
    e = PUBLIC_EXPONENT
    d = modInverse(e, co_prime)

    return (e, d, n)


def find_byte_size(int):
    if 0 < int < 255:
        return 1
    else:
        return 2


def apply_key(key, m):
    """
    Apply the key, given as a tuple (e,n) or (d,n) to the message.
    This can be used both for encryption and decryption.
    :param tuple key: (e,n) or (d,n)
    :param int m: the message as a number 1 < m < n (roughly)
    :return: the message with the key applied. For example,
             if given the public key and a message, encrypts the message
             and returns the ciphertext.
    """
    x, n = key

    return pow(m, x) % n


def break_key(pub):
    """
    Break a key.  Given the public key, find the private key.
    Factorizes the modulus n to find the prime numbers p and q.
    You can follow the steps in the "optional" part of the in-class
    exercise.
    :param pub: a tuple containing the public key (e,n)
    :return: a tuple containing the private key (d,n)
    """
    e, n = pub
    n = n
    p_q_not_found = True
    p = 0
    q = 0

    i = 2
    # take n and divide it by and increasing i until n % i equals 0
    while p_q_not_found:
        if n % i == 0:
            p = i
            q = n // p
            p_q_not_found = False
        i += 1

    co_prime = math.lcm(p - 1, q - 1)
    d = modInverse(e, co_prime)

    return d, n


def send_message():
    OTHER_HOST = input("enter the target ip address: ")
    tcp_send(OTHER_HOST, TCP_PORT)


def recv_message():
    LISTEN_ON_INTERFACE = input("Listen on target interface: ")
    tcp_receive(LISTEN_ON_INTERFACE, TCP_PORT)


# Port number definitions
# (May have to be adjusted if they collide with ports in use by other programs/services.)
# Address to listen on when acting as server.
# The address '' means accept any connection for our 'receive' port from any network interface
# on this system (including 'localhost' loopback connection).

def tcp_receive(listen_on, listen_port):
    """
    - Listen for a TCP connection on a designated "listening" port
    - Accept the connection, creating a connection socket
    - Print the address and port of the sender
    - Repeat until a zero-length message is received:
      - Receive a message, saving it to a text-file (1.txt for first file, 2.txt for second file, etc.)
      - Send a single-character response 'A' to indicate that the upload was accepted.
    - Close data connection.
    :param: int listen_port: Port number on the server to listen on
    """
    print('tcp_receive (server): listen_port={0}'.format(listen_port))
    address = (listen_on, listen_port)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    c, address = s.accept()

    (e, d, n) = create_keys()

    n_size = find_byte_size(n)
    c.send(int.to_bytes(n_size, 2, "big"))
    c.send(int.to_bytes(n, n_size, "big"))
    c.send(b'\r\n')

    e_size = find_byte_size(e)
    c.send(int.to_bytes(e_size, 2, "big"))
    c.send(int.to_bytes(e, e_size, "big"))
    c.send(b'\r\n')

    listen = True
    while listen:
        print('Connected with', address, 'through socket', c.getsockname())
        data = get_n_bytes(c, 2)
        check = get_n_bytes(c, 2)

        length = int.from_bytes(data, 'big', signed=True)

        f = open("output.txt", "a")

        i = 0
        encrypted = b""
        while i < length:
            decode_bytes = c.recv(1)
            encrypted += decode_bytes
            i += 1

        message = ""
        for i in range(0, len(encrypted), 4):
            enc_string = encrypted[i: i + 4]
            enc = int(enc_string, 16)
            dec = apply_key(get_private_key((e, d, n)), enc)
            if dec >= 0 and dec < 256:
                message += chr(dec)
            else:
                print("Warning: Could not decode encrypted entity: " + enc_string)
                print("         decrypted as: " + str(dec) + " which is out of range.")
                print("         inserting _ at position of this character")
                message += "_"

        print("Finished decoding: ", message)
        f.write(message)
        f.close()
        print("closing connection")
        c.send('A'.encode())
        listen = False

        get_n_bytes(c, 2)
        get_n_bytes(c, 2)
        c.send("Q".encode())
        s.close()


def tcp_send(server_host, server_port):
    """
    - Send multiple messages over a TCP connection to a designated host/port
    - Receive a one-character response from the 'server'
    - Print the received response
    - Close the socket
    :param str server_host: name of the server host machine
    :param int server_port: port number on server to send to
    """
    print('tcp_send: dst_host="{0}", dst_port={1}'.format(server_host, server_port))
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect((server_host, server_port))
    n_length = int.from_bytes(tcp_socket.recv(2), "big")
    n = int.from_bytes(tcp_socket.recv(n_length), "big")

    check = tcp_socket.recv(2)

    e_length = int.from_bytes(tcp_socket.recv(2), "big")

    e = int.from_bytes(tcp_socket.recv(e_length), "big")

    check2 = tcp_socket.recv(2)

    msg = input("Now enter your message: ")

    encrypted = ""
    for c in msg:
        encrypted += "{0:04x}".format(apply_key((e, n), ord(c)))

    encrypted_len = encrypted.__len__()

    tcp_socket.sendall(int.to_bytes(encrypted_len, 2, "big"))
    tcp_socket.sendall(b'\r\n')

    tcp_socket.sendall(encrypted.encode() + b"\r\n")

    print("Done sending. Awaiting reply.")
    response = tcp_socket.recv(1)
    if response == b"A":  # Note: == in Python is like .equals in Java
        print("File accepted, closing connection.")
    else:
        print("Unexpected response:", response)

    tcp_socket.sendall(b"\x00\x00")
    tcp_socket.sendall(b"\x00\x00")
    response = tcp_socket.recv(1)
    if response == b"Q":  # Reminder: == in Python is like .equals in Java
        print("Server closing connection, as expected.")
    else:
        print("Unexpected response:", response)

    tcp_socket.close()


def get_n_bytes(com, n):
    data = b''
    while len(data) < n:
        data += com.recv(1)
    return data


if __name__ == "__main__":
    main()