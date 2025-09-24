import sys
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

cSharpHeader = b'\0\x01\0\0\0\xFF\xFF\xFF\xFF\x01\0\0\0\0\0\0\0\x06\x01\0\0\0'
KEY = b'UKu52ePUBwetZ9wNX88o54dnfKRu0T1l'

def generate_length_prefixed_string(length):
    length = min(0x7FFFFFFF, length)
    b = bytearray()
    for i in range(4):
        if length >> 7 != 0:
            b.append(length & 0x7F | 0x80)
            length >>= 7
        else:
            b.append(length & 0x7F)
            length >>= 7
            break
    if length != 0:
        b.append(length)
    return b

def encrypt_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    data = json.dumps(json.loads(data.decode()), separators=(',', ':')).encode()
    print(data)
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded)
    encoded = base64.b64encode(encrypted)
    length_data = generate_length_prefixed_string(len(encoded))
    result = cSharpHeader + length_data + encoded + b'\x0B'
    with open(filename + ".dat", 'wb') as f:
        f.write(result)
    print('已加密并保存为', filename + ".dat")

def decrypt_file(filename):
    with open(filename, 'rb') as f:
        encoded = f.read()

    start = len(cSharpHeader)
    end = len(encoded)-1
    while start < end and (encoded[start] & 0x80):
        start += 1
    while end > start and (encoded[end - 1] & 0x80):
        end -= 1
    encoded = encoded[start:end]

    encrypted = base64.b64decode(encoded)
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded = cipher.decrypt(encrypted)
    data = unpad(padded, AES.block_size)
    pretty = json.dumps(json.loads(data.decode()), indent=2)
    print(pretty)

if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ['-E', '-D']:
        print('用法: python hollow_user_data.py -E|-D 文件名')
        sys.exit(1)
    if sys.argv[1] == '-E':
        encrypt_file(sys.argv[2])
    else:
        decrypt_file(sys.argv[2])
