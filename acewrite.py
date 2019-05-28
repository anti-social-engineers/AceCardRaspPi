import binascii
from Logic import *
from Encryption import *
import Adafruit_PN532 as PN532


DEFAULT_CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

temp_key = "C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS"

block_blacklist = [0, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]

CS = 18
MOSI = 23
MISO = 24
SCLK = 25

pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

def writeAce():
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
    encrypted_cardId = AESecryption(temp_key).encrypt(cardId)
    splitted_cardId_list = split_encrypted_into_blocks(encrypted_cardId)

    block_list = [40, 41, 42]
    print("Starting to write all blocks")
    for i in range(0, 3):
        if not pn532.mifare_classic_authenticate_block(uid, i, PN532.MIFARE_CMD_AUTH_A, DEFAULT_CARD_KEY):
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




