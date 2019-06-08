from BLL.Logic import *
from DAL.Encryption import *
from Libraries.Adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A

def WriteCard(pn532):
    DEFAULT_CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    print("Waiting for card...")
    uid = None
    while uid is None:
        uid = pn532.read_passive_target()
    duid = get_decoded_string(uid)
    print("Card found!! uid: {0}".format(duid))
    print('==============================================================')
    print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
    print('==============================================================')
    cardId = generateUid(duid)
    print('THE UID TO BE WRITTEN ON THE CARD: {0}'.format(cardId))
    splitted_cardId_list = split_encrypted_into_blocks(AESecryption().encrypt(cardId) + "0000")
    block_list = [40, 41, 42]
    print("Starting to write all blocks")
    for i in range(0, 3):
        print("Writing block {0}".format(block_list[i]))
        if not pn532.mifare_classic_authenticate_block(uid, block_list[i], MIFARE_CMD_AUTH_A, DEFAULT_CARD_KEY):
            print("Failed to Authenticate block, writing stopped at block: {0}".format(block_list[i]))
            raise Exception('Er is iets fout gegaan. Probeert opnieuw')
        else:
            block = block_list[i]
            if not pn532.mifare_classic_write_block(block, bytearray(splitted_cardId_list[i], "UTF-8")):
                print("Error during writing! Failed to write on block {0}", block)
                print("Cancelling writing")
                raise Exception('Er is iets mis gegaan. Probeer opnieuw')
    return cardId











