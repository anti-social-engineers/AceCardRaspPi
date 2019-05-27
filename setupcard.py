import binascii
import sys
import Adafruit_PN532 as PN532
from key import getkey
# PN532 configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Create and initialize an instance of the PN532 class.
pn532 =  PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

block_blacklist = [0, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]

print("Waiting for card...")
uid = None
while uid is None:
    uid = pn532.read_passive_target()
print("Found card with UID: {0}".format(binascii.hexlify(uid)))
print('==============================================================')
print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
print('==============================================================')

block = int(input("Which block"))
if block not in block_blacklist:
    print("Not a sector trailer!")
else:
    acekey = getkey()
    if not pn532.mifare_classic_authenticate_block(uid, block, PN532.MIFARE_CMD_AUTH_A,
                                               acekey):
        print('Error! Failed to authenticate block with the card.')
        sys.exit(-1)

    accessbits = '6B 3D 73 34 4C 29 08 77 8F FF 75 42 64 35 5f 5d'
    sectorTrailer = CARD_KEY_A + accessbits + CARD_KEY_B
    print(sectorTrailer)
    dataArray = bytearray.fromhex(accessbits)
    if not pn532.mifare_classic_write_block(block, dataArray):
        print('Error! Failed to write to the card.')
        sys.exit(-1)
    print("Acces bits have been overwritten")




