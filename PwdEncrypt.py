from cryptography.fernet import Fernet

def encrypt(bytes):
    #key = Fernet.generate_key()
    key = b'Nz0Xcsw_up4R6oJA8OqqI34dnRYvPM_pVAgabBNE4xE='
    f = Fernet(key)
    cipher = f.encrypt(bytes.encode())
    return cipher


#gAAAAABeWi8BH9wI4BU72C06ty-n6ZupCCecEK0edpQgSucJ0Vxbdf1PRE1l7VkQ4jtzyLBLulXypKfM1OZtVKKOeD6taK0Gzg==
#