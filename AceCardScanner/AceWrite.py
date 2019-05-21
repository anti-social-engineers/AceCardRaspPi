import binascii
import sys

import Adafruit_PN532 as PN532

CS   = 18
MOSI = 23
MISO = 24
SCLK = 25
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

print("Place card on the the scanner to write")
uid = pn532.read_passive_target()
while uid is None:
    uid = pn532.read_passive_target()
print(uid)
print(binascii.hexlify(uid))

print("Authenticating...")
if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                               CARD_KEY):
    print('Error! Failed to authenticate block 4 with the card.')
    sys.exit(-1)

data = bytearray("Hello world", 'ascii')

if not pn532.mifare_classic_write_block(4, data):
    print('Error! Failed to write to the card.')
    sys.exit(-1)
print("Writing succesfull")


