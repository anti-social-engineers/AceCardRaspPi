import string
import random
import sys
import binascii
import json

CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
#CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def split_encrypted_into_blocks(seq):
    if len(seq) > 48:
        print("Something went wrong during encryption")
    else:
        return [seq[i:i+16] for i in range(0, len(seq), 16)]

def generateUid(uid):
    if(len(uid)) > 8:
        print("uid too long")
        sys.exit(-1)
    else:
        chars = string.ascii_lowercase + string.digits
        return uid + ''.join(random.choice(chars) for _ in range(8))

def get_decoded_string(encoded):
    return binascii.hexlify(encoded).decode()

def login():
    with open('config.json') as json_file:
        data = json.load(json_file)
        print(data['email'])

def writejson():
    data = {'email': 'raspberry.pi@aceofclubs.nl', 'password': 'xpc^>smGBTRjKLs:Xk6&I>6&w5m~<WC-', 'encryptionkey': 'C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS'}
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

