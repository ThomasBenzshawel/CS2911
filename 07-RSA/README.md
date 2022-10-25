# Overview
In this lab, you will create and brute-force attack 16-bit RSA encryption. Before you can play out these scenarios, you will need code to create and use a public & private key.

Download and finish the file: **rsa.py**

# Requirments

Implement the three functions: create_keys, apply_key, break_key

For help on generating prime numbers see **prime_generator.py**

You can also use [this article](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) if you forget the RSA steps

Feel free to look up how to perform these steps in python: such as totient functions, coprimaility, and modular inverses

# Reflection Questions
## Question 1: RSA Security
In this lab, Trudy is able to find the private key from the public key. Why is this not a problem for RSA in practice?

## Question 2: Critical Step(s)
When creating a key, Bob follows certain steps. Trudy follows other steps to break a key. What is the difference between Bob’s steps and Trudy’s so that Bob is able to run his steps on large numbers, but Trudy cannot run her steps on large numbers?

# Checksums
In this exercise, we will pretend that we are using enough bits so that break_key is ineffective. Nevertheless, because we use a non-cryptographic hash, Alice can forge a message to look like the one Bob signed with his public key.

Bob: Run the program with the compute_checksum option to create an encrypted checksum for the message "Bob owes Trudy $100.99". Save the public & private keys, as well as the encrypted checksum for your records. Provide Alice and Trudy with the public key. Provide Trudy with the plain-text message and the encrypted checksum. (Suppose that Trudy is an unscrupulous online store)

Trudy: Create a message that results in the same checksum as Bob’s message, but implies that Bob owes a larger amount of money. Hint: If you rearrange the characters in the string, how does that change the checksum? Supply Alice with the forged message and the encrypted checksum that Bob gave you.

Alice: Check Trudy’s message using the verify_checksum option of the program. Does it check out OK? If not, Trudy should keep trying.

As a team: Explain in your final comments how Trudy can be prevented from performing this trick in a real application. (Suppose Alice is the bank responsible for transferring the money from Bob to Trudy. And note that Trudy did not use break_key here!)