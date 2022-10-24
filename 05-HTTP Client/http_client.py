from socket import *
# import the "regular expressions" module
import re

def get_http_resource(url, file_name):
    """
    Get an HTTP resource from a server
           Parse the URL and call function to actually make the request.

    :param url: full URL of the resource to get
    :param file_name: name of file in which to store the retrieved resource

    (do not modify this function)
    """

    # Parse the URL into its component parts using a regular expression.
    url_match = re.search('http://([^/:]*)(:\d*)?(/.*)', url)
    url_match_groups = url_match.groups() if url_match else []
    #    print 'url_match_groups=',url_match_groups
    if len(url_match_groups) == 3:
        host_name = url_match_groups[0]
        host_port = int(url_match_groups[1][1:]) if url_match_groups[1] else 80
        host_resource = url_match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'.format(host_name, host_port, host_resource))
        status_string = do_http_exchange(host_name.encode(), host_port, host_resource.encode(), file_name)
        print('get_http_resource: URL="{0}", status="{1}"'.format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')

# Write Helper functions here

def do_http_exchange(host, port, resource, file_name):
    """
    Get an HTTP resource from a server

    :param bytes host: the ASCII domain name or IP address of the server machine (i.e., host) to connect to
    :param int port: port number to connect to on server host
    :param bytes resource: the ASCII path/name of resource to get. This is everything in the URL after the domain name,
           including the first /.
    :param file_name: string (str) containing name of file in which to store the retrieved resource
    :return: the status code
    :rtype: int
    """
    # Open a tcp socket
    sock = socket(AF_INET, SOCK_STREAM)
    print("connected")
    # Connect the socket to the host on the given port
    sock.connect((host, port))
    # Create a request as a bytes object
    request = b'GET ' + resource + b' HTTP/1.1\r\nHost:' + host + b'\r\n\r\n'
    sock.send(request)
    # Send the request to the host
    # Receive the response for the host
    first_header = sock.recv(12)
    print(first_header.decode())
        ## Get the first line of the header first
    code = first_header[9:12]
        ## Extract the message code (e.g. 404, 200)
        ## If 200 proceeed to read the rest of the header lines
    if(code == b'200'):
        total_header = ""
        total = ""
        seen_first_r = False
        seen_first_n = False
        seen_second_r = False
        seen_second_n = False

        while not seen_second_n:
            response = sock.recv(1)
            total_header += response.decode('ascii')
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
    else:
        print(code.decode() + "Bad gateway")

    temp_string = ""
    found_encoding = False
    found_length = False

    content_length = 0

    char_location = 0
    print(total_header)
    for x in total_header:
        if (x != ':') and (x != '\n') and ((found_encoding == False) and (found_length == False)):
            temp_string += x
            char_location += 1
        elif x == ':' or x == '\n':
            if(temp_string == "Transfer-Encoding"):
                found_encoding = True
                temp_string = ""

            elif(temp_string == "Content-Length"):
                found_length = True
                temp_length_string = ""
                char_location += 1
                while temp_length_string[-2:] != '\r\n':
                    temp_length_string += total_header[char_location]
                    char_location += 1
                temp_length_string = temp_length_string[1:len(temp_length_string) - 2]
                content_length = int(temp_length_string, 16)
                temp_string = ""
            else:
                char_location += 1
                temp_string = ""

    if(found_encoding):
        chunk_length = 1
        total = b''
        while chunk_length != 0:
            temp_bytes = sock.recv(2)
            while temp_bytes[-2:] != b'\r\n':
                temp_bytes += sock.recv(1)
            chunk_length = int(temp_bytes[:-2].decode('ascii'), 16)
            data = b''
            while len(data) < chunk_length:
                data += sock.recv(1)
            print(sock.recv(2) == b'\r\n')
            total += data

        f = open(file_name, "wb")
        print(total)
        f.write(total)
        f.close()

    if (found_length):
        total = b''
        total += sock.recv(content_length)

        f = open(file_name, "wb")
        print(total)
        f.write(total)
        f.close()





    ## If the header contains the Content-Length, then
        ## Read the number of bytes given by the content length value
        ## save the bytes to a file given by file_name
    # Else if the header contains the Transfer-Encoding with value chunks
        ## Read each chunk in (remember the number that comes in with the length of the chunck is ASCII hexadecimal numbers)
        ## Combine the chunks
        ## Decode the chunks as ASCII
        ## Write the ASCII to a file given by file_name

    return int.from_bytes(code, 'big')  # Replace this "server error" with the actual status code

if __name__ == '__main__':
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('http://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('http://www.httpvshttps.com/','index.html')

    # If you find fun examples of chunked or Content-Length pages, please share them with us!