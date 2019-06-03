import binascii
import board
import busio
from digitalio import DigitalInOut
from Logic import *
from Encryption import *
from adafruit_pn532.adafruit_pn532 import *
from adafruit_pn532.spi import PN532_SPI


def writeAce():

    DEFAULT_CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    # SPI connection:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D5)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)
    pn532.SAM_configuration()
    print("Waiting for card...")
    uid = None
    while uid is None:
        uid = pn532.read_passive_target()
    duid = binascii.hexlify(uid)
    print("Card found!! uid: {0}".format(duid))
    print('==============================================================')
    print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
    print('==============================================================')

    cardId = generateUid(duid)
    temp_key = "C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS"
    encrypted_cardId = AESecryption(temp_key).encrypt(cardId) + "0000"
    splitted_cardId_list = split_encrypted_into_blocks(encrypted_cardId)

    block_list = [40, 41, 42]
    print("Starting to write all blocks")
    for i in range(0, 3):
        print("Writing block {0}".format(block_list[i]))
        if not pn532.mifare_classic_authenticate_block(uid, block_list[i], MIFARE_CMD_AUTH_A, DEFAULT_CARD_KEY):
            print("Failed to Authenticate block, writing stopped at block: {0}".format(block_list[i]))
            sys.exit(-1)
        else:
            block = block_list[i]
            if not pn532.mifare_classic_write_block(block, bytearray(splitted_cardId_list[i], "UTF-8")):
                print("Error during writing! Failed to write on block {0}", block)
                print("Cancelling writing")
                sys.exit(-1)
    print("Succesfully writting all blocks. You can safely remove the card now!")

writeAce()




