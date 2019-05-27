import binascii
import base64, uuid
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
from key import getkey

# BS = 32
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
# unpad = lambda s : s[:-ord(s[len(s)-1:])]
#

# salt = uuid.uuid4().hex
# x = uid + salt
# print()
# print(len(x))
#
# key = hashlib.sha256('p3s6v9y$B&E)H@McQfTjWmZq4t7w!z%C*F-JaNdRgUkXp2r5u8x/A?D(G+KbPeSh'.encode()).digest()
#
# message = pad(x)
# iv = Random.new().read(AES.block_size)
# cipher = AES.new(key, AES.MODE_CBC, iv)
# encr = base64.b64encode(iv + cipher.encrypt(message.encode()))
#
# print("ENCRRR")
# print(len(encr))
#
# enc = base64.b64decode(encr)
# iv1 = enc[:AES.block_size]
# c = AES.new(key, AES.MODE_CBC, iv1)
# dec = unpad(c.decrypt(enc[AES.block_size:]).decode('utf-8'))
# print(dec)


# x = '1234abcd'
# f = bytearray(x, 'utf-8')
# print(f)
# print(f.decode('utf-8'))
# f = bytearray(base64.b64encode(f))
# length = int(len(f) /2)
# a = f[0:length]
# print("here {0}".format(a))
#
#
# p = f.decode('utf-8')
#
#
# s = base64.b64decode(p).decode('utf-8')

# print(s)


key = hashlib.sha256('C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS'.encode()).digest()
iv = Random.new().read(AES.block_size)
aes = AES.new(key, AES.MODE_CBC, iv)
data = '1234567812345678'
encr = base64.b64encode(aes.encrypt(data.encode()))
print(len(encr))
z = bytearray(encr)
print(z)


enc = base64.b64decode(z)
print(enc)
aec = AES.new(key, AES.MODE_CBC, iv)
decd = (aec.decrypt(enc)).decode()

print(decd)

# dataHex = binascii.unhexlify(data)
#     # dataArray = bytearray(dataHex)
#     text = string.ascii_letters + string.digits
#     x = uid + ''.join(random.sample(text, 8))



# x = bytearray('000000000000000'.encode('utf-8'))
# print(x)
#
# data = x
# test = bytearray(data).decode('utf-8')
#
# print(test)
#


# CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
# CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]
#
# CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
#
# test = bytearray(CARD_KEY_A + [0x08, 0x77, 0x8F, 0xFF] + CARD_KEY_B).hex()
# s = " ".join(test[i:i+2] for i in range(0, len(test), 2))
#
#
# CARD_KEY_A1 = '6B 3D 73 34 4C 29'
# CARD_KEY_B1 = '75 42 64 35 5f 5d'
# f = (CARD_KEY_A1 + ' ' + '08 77 8F FF' + ' ' + CARD_KEY_B1)

# print('6B 3D 73 34 4C 29 08 77 8F FF 75 42 64 35 5f 5d' == f)
# print(test)
# print(s)




CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]