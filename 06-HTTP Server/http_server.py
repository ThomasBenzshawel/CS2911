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
    # Get the request line
    try:
        request_header = read_request_header(request_socket)
        resource = get_data_wanted(request_header)
        code, status = get_status(request_header, request_socket)
        message = build_response(resource, code, status)
    except BaseException:
        message = b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
    request_socket.sendall(message)

def read_request_header(sock) -> list:
    request = read_line(sock)
    while request[-4:] != b'\r\n\r\n':
        request += read_line(sock)
    header = request.split(b'\r\n')
    while request[-1] == b'':
        header.pop(-1)
    return header

def get_data_wanted(header: list) -> str:
    file_name = header[0].split(b' ')[1].decode('ASCII')
    if file_name == '/':
        file_name = 'index.html'
    else:
        file_name = file_name[1:]
    return file_name
def read_line(sock):
    line = sock.recv(1)
    while line[-2:] != b'\r\n':
        line += sock.recv(1)
    return line

def get_status(request: list, sock=None) -> tuple:
    first_line_items = request[0].split(b' ')
    command = first_line_items[0]
    resource = get_data_wanted(request)
    if command.lower() == b'GET'.lower():
        if first_line_items[-1] != b'HTTP/1.1':
            return b'400', b'Bad Request'
        if os.path.isfile(resource):
            return b'200', b'OK'
        else:
            return b'404', b'Not Found'
    elif sock is not None:
        return put_status(request, get_body(get_content_length(request), sock))
    else:
        return b'400', b'Bad Request'

def put_status(header: list, body: bytes) -> tuple:
    first_line_items = header[0].split(b' ')
    command = first_line_items[0]
    resource = get_data_wanted(header)
    if command.lower == b'PUT'.lower() and first_line_items[-1] == b'HTTP/1.1':
        if os.path.isfile(resource):
            if write_to_file(resource, body):
                return b'200', b'OK'
            else:
                return b'500', b'Internal Server Error'
        elif write_to_file(resource, body):
            return b'201', b'Created'
        else:
            return b'500', b'Internal Server Error'
    else:
        return b'400', b'Bad Request'

def write_to_file(file_name: str, content: bytes):
    try:
        with open(file_name, 'wb') as file:
            file.write(content)
        file.close()
        return True
    except BaseException:
        return False

def get_body(length: int, sock: socket) -> bytes:
    body = b''
    for i in range(length):
        body += sock.recv(1)
    return body

def get_content_length(header: list) -> int:
    content_length = 0
    for i in range(len(header)):
        if header[i].containts(b'Content-length:'):
            length = header[i].split(b' ')[1]
            for j in range(len(length)):
                content_length += (int(length[j].decode('ASCII')) - 0x30) * (10 ** (len(length) - j - 1))
    return content_length

def build_response(file_path, stat_code, stat_message) -> bytes:
    response = build_header(file_path, stat_code, stat_message) + build_body(file_path, stat_code)
    return response

def build_header(file_path, stat_code, stat_message) -> bytes:
    header_dictionary = build_header_string(file_path)
    header = b'HTTP/1.1 ' + stat_code + b' ' + stat_message + b'\r\n'
    # Creates the key-value section of the header
    for key in header_dictionary.keys():
        header += key + b': ' + header_dictionary[key] + b'\r\n'
    header += b'\r\n'
    return header


def build_header_string(file_path):
    header_dictionary = {}
    timestamp = datetime.datetime.utcnow()
    timestring = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    date_header = timestring.encode('ASCII')
    header_dictionary[b'Date'] = date_header
    header_dictionary[b'Connection'] = b'close'
    if get_mime_type(file_path) is not None:
        header_dictionary[b'Content-Type'] = get_mime_type(file_path).encode('ASCII')
    if get_file_size(file_path) is not None:
        header_dictionary[b'Content-Length'] = str(get_file_size(file_path)).encode('ASCII')
    return header_dictionary

def build_body(resource, stat_code) -> bytes:
    if stat_code == b'200':
        with open(resource, 'rb') as file:
            contents = file.read()
        file.close()
        return contents
    else:
        return b''

def file_exists(file_name) -> bool:
    try:
        with open(file_name, 'r') as file:
            return True
    except FileNotFoundError:
        return False


if __name__ == '__main__':
    # Start the server
    http_server_setup(8080)
    # Now  navigate to localhost:8080 in your browser