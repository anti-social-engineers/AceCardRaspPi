import binascii
import sys
from Logic import *
from Encryption import *
import Adafruit_PN532 as PN532

if __name__ == '__main__':
    CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]
    # Configuration for a Raspberry Pi:
    CS = 18
    MOSI = 23
    MISO = 24
    SCLK = 25

    # Create an instance of the PN532 class.
    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    pn532.begin()

    def readAce(key, pn532init):

        temp_key = "C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS"


        print("Place the card on the Scanner")
        while True:
            uid = pn532init.read_passive_target()
            if uid is not None:
                print('Found card with UID: {0}'.format((binascii.hexlify(uid))))
                encrypted_cardId = ""
                block_list = [40, 41, 42]
                for i in range(0, 3):
                    if not pn532init.mifare_classic_authenticate_block(uid, block_list[i], PN532.MIFARE_CMD_AUTH_B, key):
                        print("Failed to Authenticate block, reading stopped at block: {0}".format(block_list[i]))
                        sys.exit(-1)
                    else:
                        block_data = bytearray(pn532init.mifare_classic_read_block(block_list[i])).decode("UTF-8")
                        if block_data is not None:
                            encrypted_cardId += block_data
                        else:
                            print("No data to be found on block {0}".format(block_list[i]))
                print("All blocks are read, decrypting now....")
                encrypted_cardId = encrypted_cardId[0:45]
                decrypted_cardId = AESecryption(temp_key).decrypt(encrypted_cardId)
                print('==============================================================')
                print('CARD ID FOUND: {0}'.format(decrypted_cardId))
                print('==============================================================')
            else:
                continue

    readAce(CARD_KEY_B, pn532)