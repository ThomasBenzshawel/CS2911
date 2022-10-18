from socket import *
import re
import threading
import os
import mimetypes
import datetime

def http_server_setup(port):
    """
    Start the HTTP server
    - Open the listening socket
    - Accept connections and spawn processes to handle requests

    :param port: listening port number
    """

    num_connections = 10
    server_socket = socket(AF_INET, SOCK_STREAM)
    listen_address = ('', port)
    server_socket.bind(listen_address)
    server_socket.listen(num_connections)
    try:
        while True:
            request_socket, request_address = server_socket.accept()
            print('connection from {0} {1}'.format(request_address[0],
                                                   request_address[1]))
            # Create a new thread, and set up the handle_request method and its argument (in a tuple)
            request_handler = threading.Thread(target=handle_request,
                                               args=(request_socket, ))
            # Start the request handler thread.
            request_handler.start()
            # Just for information, display the running threads (including this main one)
            print('threads: ', threading.enumerate())
    # Set up so a Ctrl-C should terminate the server; this may have some problems on Windows
    except KeyboardInterrupt:
        print("HTTP server exiting . . .")
        print('threads: ', threading.enumerate())
        server_socket.close()

# You may use these functions to simplify your code.
def get_mime_type(file_path):
    """
    Try to guess the MIME type of a file (resource), given its path (primarily its file extension)

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If successful in guessing the MIME type, a string representing the content type, such as 'text/html'
             Otherwise, None
    :rtype: int or None
    """

    mime_type_and_encoding = mimetypes.guess_type(file_path)
    mime_type = mime_type_and_encoding[0]
    return mime_type


def get_file_size(file_path):
    """
    Try to get the size of a file (resource) as number of bytes, given its path

    :param file_path: string containing path to (resource) file, such as './abc.html'
    :return: If file_path designates a normal file, an integer value representing the the file size in bytes
             Otherwise (no such file, or path is not a file), None
    :rtype: int or None
    """

    ##Syncing repository

    # Initially, assume file does not exist
    file_size = None
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
    return file_size

def handle_request(request_socket):
    i = 0
    # Get the request line
    request_line = ""
    current_byte = b''
    while current_byte != b'\n':
        current_byte = request_socket.recv(1)
        request_line += current_byte.decode()

    print(request_line)
    # Get the remaining header lines
    seen_first_r = False
    seen_first_n = False
    seen_second_r = False
    seen_second_n = False

    total_response = ""

    while not seen_second_n:
        response = request_socket.recv(1)
        total_response += response.decode()
        if response == b'\r' and seen_first_r == False:
            seen_first_r = True
        elif seen_first_r and response == b'\n':
            seen_first_n = True

        if seen_first_r and seen_first_n and response == b'\r':
            seen_second_r = True
        elif seen_first_r and seen_first_n and response != b'\n':
            seen_first_r = False
            seen_first_n = False

        if seen_first_r and seen_first_n and seen_second_r and response == b'\n':
            seen_second_n = True
    # if request is "/"
    print(total_response)
    if(request_line[4] == '/'):
        i = 4
        total_request = ""
        while(request_line[i] != " "):
            total_request += request_line[i]
            i += 1

        # build response line
        response_line = "HTTP/1.1 200 \r\n".encode()
        response_line += " OK\r\n".encode()
        request_socket.send(response_line)
        # build response headers

        # get index.html as bytes
        # send response, headers, and index.html
    # if request matches any file in current dir
        # build response line
        # build response headers
        # get file as bytes
        # send response, headers, and file
    # else
        # build 404 Not Found response line
        # build response headers
        # send back response and headers
    # close request socket

if __name__ == '__main__':
    # Start the server
    http_server_setup(8080)
    # Now  navigate to localhost:8080 in your browser