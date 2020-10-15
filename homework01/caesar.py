import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.isalpha() == True:
            if (i == "z") or (i == "Z") or (i == "y") or (i == "Y") or (i == "x") or (i == "X"):
                ciphertext += chr(ord(i) - 23)
            else:
                ciphertext += chr(ord(i) + shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.isalpha() == True:
            if (i == "a") or (i == "A") or (i == "b") or (i == "B") or (i == "c") or (i == "C"):
                plaintext += chr(ord(i) + 23)
            else:
                plaintext += chr(ord(i) - shift)
        else:
            plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    for i in dictionary:
        if len(i) == len(ciphertext):
            if (ord(ciphertext[0]) < ord(i[0])):
                k = ord(ciphertext[0]) + 26 - ord(i[0])
            else:
                k = ord(ciphertext[0]) - ord(i[0])
            for j in range(len(i)):
                if (ord(ciphertext[0]) < ord(i[0])):
                    k1 = ord(ciphertext[j]) + 26 - ord(i[j])
                else:
                    k1 = ord(ciphertext[j]) - ord(i[j])
                if k != k1:
                    break
                else:
                    best_shift = k
    return best_shift