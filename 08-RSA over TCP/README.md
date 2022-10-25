# Overview
In this lab, you will use the code from lab 07-RSA to send secret messages over tcp

# Requirments
You need to add a loop to your previous lab such that after each user input you loop back up again.

You should add an option to start a server that does the following on the port of your choice:
- waits for a connection
- upon receiving a connection generates and sends a public key tuple
- immediately after receive a message from the client
- decrypt and print that message
- send a b'A' then close the connection

You should add an option to start a client that does the following on the port of your choice:
- creates a connection to a server
- immediately after receive a public key tuple
- encrypt and send a message then close the connection
- receive a b'A' and then close the connection