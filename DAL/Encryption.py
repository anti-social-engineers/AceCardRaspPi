from Crypto.Cipher import AES
from DAL.ApiController import openConfig
import base64
import os

class AESecryption:

    def __init__(self):
        self.key = self.getKey()

    def getKey(self):
        data = openConfig()
        return data['Encryptionkey'].encode("UTF-8")

    def encrypt(self, cardId):
        cardId_byte_array = cardId.encode("UTF-8")
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_cardId = cipher.encrypt(cardId_byte_array)
        return base64.b64encode(iv + encrypted_cardId).decode("UTF-8")

    def decrypt(self, encrypted_cardId):
        decoded = base64.b64decode(encrypted_cardId)

        # first 16 bytes are the initialization vector
        iv = decoded[0:16]

        # the remaining bytes is the encrypted card Id
        messagebytes = decoded[16:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(messagebytes).decode("UTF-8")




