

def decimal_to_binary(num):
    if num == 0:
        return "0"

    binary = ""

    while num > 0:
        remainder = num % 2
        binary = str(remainder) + binary
        num = num // 2

    return binary


# Driver code
number = 22
print("Decimal:", number)
print("Binary:", decimal_to_binary(number))


def binary_to_decimal(binary):
    decimal = 0
    power = 0

    # Traverse from right to left
    for digit in binary[::-1]:
        if digit == '1':
            decimal += 2 ** power
        power += 1

    return decimal


# Driver code
binary = "1010"
print("Binary:", binary)
print("Decimal:", binary_to_decimal(binary))


# DECIMAL TO OCTAL
def decimal_to_octal(num):
    if num == 0:
        return "0"
        

    octal = ""

    while num > 0:
        remainder = num % 8
        octal = str(remainder) + octal
        num = num // 8

    return octal


# Driver code
number = 123
print("Decimal:", number)
print("Octal:", decimal_to_octal(number))

# OCTAL TO DECIMAL
def octal_to_decimal(octal):
    decimal = 0
    power = 0

    # Traverse from right to left
    for digit in octal[::-1]:
        decimal += int(digit) * (8 ** power)
        power += 1

    return decimal


# Driver code
octal = "173"
print("Octal:", octal)
print("Decimal:", octal_to_decimal(octal))

# DECIMAL TO HEXADECIMAL
def decimal_to_hex(num):
    if num == 0:
        return "0"

    hex_digits = "0123456789ABCDEF"
    hexa = ""

    while num > 0:
        remainder = num % 16
        hexa = hex_digits[remainder] + hexa
        num = num // 16

    return hexa


# Driver code
number = 123
print("Decimal:", number)
print("Hexadecimal:", decimal_to_hex(number))


# BINARY TO OCTAL

def binary_to_octal(binary):
    decimal = 0

    # Binary to Decimal
    power = 0
    for digit in binary[::-1]:
        decimal += int(digit) * (2 ** power)
        power += 1

    # Decimal to Octal
    if decimal == 0:
        return "0"

    octal = ""
    while decimal > 0:
        octal = str(decimal % 8) + octal
        decimal //= 8

    return octal


# Driver code
binary = "1010"
print("Binary:", binary)
print("Octal:", binary_to_octal(binary))

# OCTAL TO BINARY

def octal_to_binary(octal):
    # Step 1: Octal to Decimal
    decimal = 0
    power = 0

    for digit in octal[::-1]:
        decimal += int(digit) * (8 ** power)
        power += 1

    # Step 2: Decimal to Binary
    if decimal == 0:
        return "0"

    binary = ""
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal //= 2

    return binary


# Driver code
octal = "24"
print("Octal:", octal)
print("Binary:", octal_to_binary(octal))


# BINARY TO HEXADECIMAL

def binary_to_hex(binary):
    # Step 1: Binary to Decimal
    decimal = 0
    power = 0

    for digit in binary[::-1]:
        decimal += int(digit) * (2 ** power)
        power += 1

    # Step 2: Decimal to Hexadecimal
    hex_digits = "0123456789ABCDEF"

    if decimal == 0:
        return "0"

    hexa = ""
    while decimal > 0:
        hexa = hex_digits[decimal % 16] + hexa
        decimal //= 16

    return hexa


# Driver code
binary = "1010"
print("Binary:", binary)
print("Hexadecimal:", binary_to_hex(binary))


# OCTAL TO HEXADECIMAL

def octal_to_hex(octal):
    # Step 1: Octal to Decimal
    decimal = 0
    power = 0

    for digit in octal[::-1]:
        decimal += int(digit) * (8 ** power)
        power += 1

    # Step 2: Decimal to Hexadecimal
    hex_digits = "0123456789ABCDEF"

    if decimal == 0:
        return "0"

    hexa = ""
    while decimal > 0:
        hexa = hex_digits[decimal % 16] + hexa
        decimal //= 16

    return hexa


# Driver code
octal = "247"
print("Octal:", octal)
print("Hexadecimal:", octal_to_hex(octal))


# HEXADECIMAL TO OCTAL

def hex_to_octal(hexa):
    hex_digits = "0123456789ABCDEF"

    # Step 1: Hexadecimal to Decimal
    decimal = 0
    power = 0

    for digit in hexa[::-1]:
        value = hex_digits.index(digit.upper())
        decimal += value * (16 ** power)
        power += 1

    # Step 2: Decimal to Octal
    if decimal == 0:
        return "0"

    octal = ""
    while decimal > 0:
        octal = str(decimal % 8) + octal
        decimal //= 8

    return octal


# Driver code
hexa = "A7"
print("Hexadecimal:", hexa)
print("Octal:", hex_to_octal(hexa))
