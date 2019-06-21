from BLL.CustomErrors import NFCScanError
import string
import random
import binascii
import json


CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

"""
Split the 48 character long encrypted card code 
into 3 parts of max 16 bytes to write on the seperate blocks
"""

def split_encrypted_into_blocks(seq):
    if len(seq) > 48:
        print("Something went wrong during encryption")
    else:
        return [seq[i:i+16] for i in range(0, len(seq), 16)]

"""
Since we use AES encryption and not make use of padding I add 8 characters 
to the already 8 long unique manufacturer card Id
"""
def generateUid(uid):
    if(len(uid)) > 8:
        raise NFCScanError
    else:
        chars = string.ascii_lowercase + string.digits
        return uid + ''.join(random.choice(chars) for _ in range(8))

def get_decoded_string(encoded):
    return binascii.hexlify(encoded).decode()