# Definitions to read bytes from a file

file = None


def set_file(filename):
    """
    Set the file name for the file to read
    Open the file and close any one that is already open
    :param filename: path to the file
    """
    global file
    if file is not None:
        file.close()
    file = open(filename, "rb")


def read_byte():
    """
    Read the next byte from the file
    Raise an error if the file is not set or has no more data
    """
    global file
    if file is None:
        raise EOFError
    rv = file.read(1)
    if len(rv) == 0:
        raise EOFError
    return rv
