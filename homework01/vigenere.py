def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    if len(plaintext) > len(keyword):
        keyword *= (len(plaintext) // len(keyword)) + 1
    kwcp = keyword.upper()
    for i in range(len(plaintext)):
        j = ord(plaintext[i]) + ord(kwcp[i]) - 65
        s = ord(plaintext[i])
        if (j > 90) and (s < 91):
            if plaintext[i].isalpha() == True:
                ciphertext += chr(ord(plaintext[i]) + ord(kwcp[i]) - 65 - 26)
            else:
                ciphertext += plaintext[i]
        elif (j <= 90) and (s < 91):
            if plaintext[i].isalpha() == True:
                ciphertext += chr(ord(plaintext[i]) + ord(kwcp[i]) - 65)
            else:
                ciphertext += plaintext[i]
        elif (s > 96) and (j > 122):
            if plaintext[i].isalpha() == True:
                ciphertext += chr(ord(plaintext[i]) + ord(kwcp[i]) - 65 - 26)
            else:
                ciphertext += plaintext[i]
        else:
            if plaintext[i].isalpha() == True:
                ciphertext += chr(ord(plaintext[i]) + ord(kwcp[i]) - 65)
            else:
                ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    if len(ciphertext) > len(keyword):
        keyword *= (len(ciphertext) // len(keyword)) + 1
    kwcp = keyword.upper()
    for i in range(len(ciphertext)):
        j = ord(ciphertext[i]) - ord(kwcp[i]) + 65
        s = ord(ciphertext[i])
        if (j < 65) and (s < 91):
            if ciphertext[i].isalpha() == True:
                plaintext += chr(ord(ciphertext[i]) - ord(kwcp[i]) + 65 + 26)
            else:
                plaintext += ciphertext[i]
        elif (j >= 65) and (s < 91):
            if ciphertext[i].isalpha() == True:
                plaintext += chr(ord(ciphertext[i]) - ord(kwcp[i]) + 65)
            else:
                plaintext += ciphertext[i]
        elif (s > 96) and (j < 96):
            if ciphertext[i].isalpha() == True:
                plaintext += chr(ord(ciphertext[i]) - ord(kwcp[i]) + 65 + 26)
            else:
                plaintext += ciphertext[i]
        else:
            if ciphertext[i].isalpha() == True:
                plaintext += chr(ord(ciphertext[i]) - ord(kwcp[i]) + 65)
            else:
                plaintext += ciphertext[i]
    return plaintext
