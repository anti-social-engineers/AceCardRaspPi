import binascii
import sys
import Adafruit_PN532 as PN532

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

pn532.SAM_configuration()

print("Waiting for Ace card...")

while True:
    uid = pn532.read_passive_target()
    if uid is not None:
        print("UID = " + str(binascii.hexlify(uid)))
        break
    else:
        continue

if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
    print('Failed to authenticate block 4!')

data = pn532.mifare_classic_read_block(4)
if data is None:
    print('Failed to read block 4!')
print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))



