import binascii
import sys

import Adafruit_PN532 as PN532

# Configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25

# Create an instance of the PN532 class.
def test():

  pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
  key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
  pn532.begin()

  ic, ver, rev, support = pn532.get_firmware_version()
  
  while True:
      uid = pn532.read_passive_target()
      if uid is not None:
          return 'Found card with UID: {0}'.format((binascii.hexlify(uid)))

