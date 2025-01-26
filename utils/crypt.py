import uuid
from cryptography.fernet import Fernet

def get_windows_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ''.join(mac[i:i+2] for i in range(0, 12, 2))

def encrypt_mac_address(mac_address, encryption_key):
    cipher = Fernet(encryption_key)
    encrypted_mac = cipher.encrypt(mac_address.encode())
    return encrypted_mac

def decrypt_mac_address(encrypted_mac, encryption_key):
    try:
        cipher = Fernet(encryption_key)
        decrypted_mac = cipher.decrypt(encrypted_mac).decode()
        return decrypted_mac
    except Exception as e:
        return ''

# Get the MAC address
# mac_address = get_windows_mac_address()
# print(f"MAC Address: {mac_address}")
# encrypted_mac = encrypt_mac_address("88a4c22cdd42", b'NxhLBBnSCAsWT_I-fxUIJqfRGI4SoG-1bqpS4nhcPR0=')
# print(f"Encrypted MAC Address: {encrypted_mac}")
