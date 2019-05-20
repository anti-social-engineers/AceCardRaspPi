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
        print(binascii.hexlify(uid))
        break
    else:
        continue

print("Card Found!")


