#
# Write a function that takes an int and returns a string
# of the binary representation as given by the bin() function
# do not use bin()
#
def int_bits(x):
    returned = ""
    negative = False
    if x < 0:
        negative = True
        x = -x
    while x // 2 > 0:
        y = x % 2
        returned += str(y)
        x = x // 2

    if x == 1:
        returned += "1"
    else:
        returned += "0"

    returned = returned[::-1]
    if negative:
        finalreturn = "-0b" + returned
    else:
        finalreturn = "0b" + returned
    return finalreturn

#
# Write a function that takes an ascii string and returns a string of
# the underyling binary representation stored by the computer
# as byte length chunks
# ex: 'Hi' -> '01101000 01101001'
#
def str_bits(x):
    i = 0
    returned = ""

    while i < len(x):
        temp = x[i]
        temp = ord(temp)
        temp = bin(temp)
        temp = temp[2:]
        returned += "0" + str(temp) + " "
        i += 1

    return returned[:-1]

def int_bits_ascii(x):
    x = int(x)
    returned = ""

    while x // 2 > 0:
        y = x % 2
        returned += str(y)
        x = x // 2

    if x == 1:
        returned += "1"
    else:
        returned += "0"

    returned = returned[::-1]
    return returned

#
# Write a function that takes a bytes object and returns a string of
# the underyling binary representation stored by the computer
# as byte length chunks
# ex: b'Hi' -> '01001000 01101001'
# ex: b'\x48\x69' -> '01001000 01101001'
#
def bytes_bits(x):
    returned = ""
    l = list(x)

    for ch in l:
        temp = int_bits_ascii(ch)
        returned += "0" + temp + " "
    return returned[:-1]

#x.to_bytes(4, 'big', signed=True)
#int.from_bytes(y, 'big', signed=true)

#
# Write a function that takes an int and returns a string
# of the hex representation
#
def int_hex(x):
    return hex(x)


#
# Write a function that takes an ascii string and returns a string of
# the underyling hex representation stored by the computer
# as byte length chunks
# ex: 'Hi' -> '0x4869'
#
def str_hex(x):
    returned = "0x"
    l = list(x)

    for ch in l:
        y = hex(ord(ch))
        returned += y[2:]
    return returned


#
# Write a function that takes a bytes object and returns a string of
# the underyling hex representation stored by the computer
# ex: b'Hi' -> '0x4869'
# ex: b'\x48\x69' -> '0x4869'
#
def bytes_hex(x):
    returned = "0x"
    l = list(x)

    for ch in l:
        y = hex(ch)
        returned += y[2:]
    return returned


#
# Take a binary string -- '0b...' -- and convert to an int
#
def bin_int(x):
    total = 0
    negative = False
    if x[0] == "-":
        negative = True

    if negative:
        y = x[3:]
    else:
        y = x[2:]

    i = len(y) - 1
    base2 = 1

    while i >= 0:
        total += base2 * int(y[i])
        base2 *= 2
        i -= 1

    if negative:
        total *= -1
    return total

#
# Take a bytes object -- b'...' and convert to an int
# Make sure you use big endian and signed conversion
#
def bytes_int(x):
    return int.from_bytes(x, 'big', signed=True)


#
# Take an int and convert to bytes object
# Make sure you use big endian and signed conversion
#
def int_bytes(x):
    if(x < 10 and x > 0):
        y = x.to_bytes(1, 'big', signed=True)
    else:
        y = x.to_bytes(2, 'big', signed=True)
    return y


#
# Take an string and convert to bytes object
#
def str_bytes(x):
    return bytes(x, 'ascii')


#
# Take a byte and convert to string object
#
def bytes_str(x):
    return str(x, 'UTF-8')
