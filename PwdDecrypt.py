from cryptography.fernet import Fernet

def decrypt(cipher):
    key = b'Nz0Xcsw_up4R6oJA8OqqI34dnRYvPM_pVAgabBNE4xE='
    f = Fernet(key)
    decoded = f.decrypt(cipher)
    return decoded

