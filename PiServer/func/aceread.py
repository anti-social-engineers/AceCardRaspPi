import binascii
import sys

import Adafruit_PN532 as PN532

def Read():

# Configuration for a Raspberry Pi:
  CS   = 18
  MOSI = 23
  MISO = 24
  SCLK = 25

# Create an instance of the PN532 class.
  pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
  key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
  pn532.begin()
  CardContent = ""
  ic, ver, rev, support = pn532.get_firmware_version()
  CardContent += (('Found PN532 with firmware version: {0}.{1}'.format(ver, rev)) + "\n")


  while True:
      uid = pn532.read_passive_target()
      if uid is not None:
          CardContent += (('Found card with UID: {0}'.format((binascii.hexlify(uid)))) + "\n")
          blocks = {5, 10, 12, 18, 20, 25, 30, 37, 41, 46, 48, 54, 57, 62}
          
          for block in blocks:
            if not pn532.mifare_classic_authenticate_block(uid, block, PN532.MIFARE_CMD_AUTH_B, key):
                CardContent += (('Failed to authenticate block {0}!'.format(block)) + "\n")
            else:
                data = pn532.mifare_classic_read_block(block)
                if data is None:
                    CardContent += (('Failed to read block {0}!'.format(block)) + "\n")
                else:
                    CardContent += (('Reading block {0}: {1}'.format(block, binascii.hexlify(data))) + "\n")
          return CardContent
      else:
          continue

