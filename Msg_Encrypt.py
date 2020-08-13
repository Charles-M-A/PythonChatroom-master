def mencrypt(msg = bytearray(4096)):
    key = 2
    result = ""
    text = msg.decode()
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + key - 65) % 26 + 65)
        else:
            result += chr((ord(char) + key - 97) % 26 + 97)
    print(result)
    return result.encode()


def mdecrypt(msg = bytearray(4096)):
    key = 2
    result = ""
    text = msg.decode()
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) - key - 65) % 26 + 65)
        else:
            result += chr((ord(char) - key - 97) % 26 + 97)
    return result.encode()
