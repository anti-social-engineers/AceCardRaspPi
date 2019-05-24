import binascii
import sys
import random
import string

import Adafruit_PN532 as PN532

# PN532 configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

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
print("LENGTH OF UID = {0}".format(len(binascii.hexlify(uid))))
print('==============================================================')
print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
print('==============================================================')

block = int(input("Which block"))
if block in block_blacklist:
    print("Not allowed to write in sector trailers!")
else:
    if not pn532.mifare_classic_authenticate_block(uid, block, PN532.MIFARE_CMD_AUTH_B,
                                               CARD_KEY):
        print('Error! Failed to authenticate block with the card.')
        sys.exit(-1)

    data = 'abcd1234abcd1234'
    dataArray = bytearray(data, 'utf-8')
    if not pn532.mifare_classic_write_block(block, dataArray):
        print('Error! Failed to write to the card.')
        sys.exit(-1)




