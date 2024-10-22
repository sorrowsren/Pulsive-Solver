import json
import base64
import hashlib
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def cryptojsDecrypt(raw_data, key):
    data = json.loads(raw_data)

    salt = bytes.fromhex(data['s'])

    salted = ""
    dx = b''

    for _ in range(3):
        dx = hashlib.md5(dx + key.encode('utf-8') + salt).digest() # Hashing previous md5 hash (or empty string if it's the first hash) + key + salt
        salted += dx.hex() # Adding hash result to salted
    
    aes_key = bytes.fromhex(salted[:64])
    iv = bytes.fromhex(data['iv'])
    aes = AES.new(aes_key, AES.MODE_CBC, iv)

    cipher_text = base64.b64decode(data['ct'])
    decrypted_data = unpad(aes.decrypt(cipher_text), AES.block_size)
    
    return decrypted_data.decode('utf-8')

def cryptojsEncrypt(data, key, switchOrder):
    salt = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

    salted = ""
    dx = b''

    for _ in range(3):
        dx = hashlib.md5(dx + key.encode('utf-8') + salt.encode('utf-8')).digest() # Hashing previous md5 hash (or empty string if it's the first hash) + key + salt
        salted += dx.hex() # Adding hash result to salted

    aes_key = bytes.fromhex(salted[:64])
    iv = bytes.fromhex(salted[64:96])

    aes = AES.new(aes_key, AES.MODE_CBC, iv)

    padded_data = pad(data.encode('utf-8'), AES.block_size)
    cipher_text = aes.encrypt(padded_data)

    encrypted_data = {
        'ct': base64.b64encode(cipher_text).decode('utf-8'),
        'iv': iv.hex(),
        's': salt.encode('utf-8').hex()
    }

    if switchOrder:
        encrypted_data = {
            'ct': base64.b64encode(cipher_text).decode('utf-8'),
            's': salt.encode('utf-8').hex(),
            'iv': iv.hex(),
        }

    return json.dumps(encrypted_data, separators=(',', ':'))