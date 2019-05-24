import binascii
import sys

import Adafruit_PN532 as PN532

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Create an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
pn532.begin()

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))


while True:
    uid = pn532.read_passive_target()
    if uid is not None:
        print('Found card with UID: {0}'.format((binascii.hexlify(uid))))
        block = int(input("Which block to read?"))
        if not pn532.mifare_classic_authenticate_block(uid, block, PN532.MIFARE_CMD_AUTH_B,
                                                       key):
            print('Failed to authenticate block {0}!'.format(block))
            continue
        else:
            data = pn532.mifare_classic_read_block(block)
            if data is None:
                print('Failed to read block {0}!'.format(block))
                continue
            else:
                print('Reading block {0}: {1}'.format(block, data.decode('utf-8')))
    else:
        continue



