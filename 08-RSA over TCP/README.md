# Overview
In this lab, you will use the code from lab 07-RSA to send secret messages over tcp

# Requirments
You need to add a loop to your previous lab such that after each user input you loop back up again.

You should add an option to start a server that does the following on the port of your choice:
- waits for a connection
- upon receiving a connection generates public key tuple
    - Send 2 bytes (m) that represent the size in bytes of your modulus n
    - Send the public modulus n using int.to_bytes(n, m, 'big')
    - Send a following '\r\n'
    - Send 2 bytes (m) that represent the size in bytes of your public exponent e
    - Send the public exponent e using int.to_bytes(e, m, 'big')
    - Send a following '\r\n'
- immediately after receive a message from the client
    - The first 2 bytes (m) represent the size in bytes of the message
    - The message will be followed by a trailing '\r\n'
- decrypt and print that message
- send a b'A' then close the connection

You should add an option to start a client that does the following on the port of your choice:
- creates a connection to a server
- immediately after receive a public key tuple
    - receive 2 bytes (D) and decode with m = int.from_bytes(D, 'big')
    - receive m bytes (D), and then decode with n = int.from_bytes(D, 'big')
    - receive '\r\n'
    - repeat for pulbic exponent e
- encrypt and send a message
    - Create a plaintext ASCII message
    - Encrypt
    - Send 2 bytes (m) that give the size of the message in bytes
    - Send encrypted messsage
    - Send '\r\n'
- receive a b'A' and then close the connection

# Grading

Demonstrate both the client and server functionality by sending encrypted messaged between the instructor and yourself