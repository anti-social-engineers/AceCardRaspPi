import binascii
import base64, uuid
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

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

key = hashlib.sha256('p3s6v9y$B&E)H@McQfTjWmZq4t7w!z%C*F-JaNdRgUkXp2r5u8x/A?D(G+KbPeSh'.encode()).digest()
iv = Random.new().read(AES.block_size)
aes = AES.new(key, AES.MODE_CBC, iv)
data = '1234567812345678'
encr = base64.b64encode(aes.encrypt(data.encode()))
print(len(encr))
print(encr)

enc = base64.b64decode(encr)
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
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
print(type(bytearray(CARD_KEY)))