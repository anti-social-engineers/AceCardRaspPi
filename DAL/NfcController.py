from BLL.Logic import *
from Libraries.Adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from DAL.Encryption import *

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
            raise Exception('Kon kaart niet authentificeren. Probeer opnieuw')
        else:
            block = block_list[i]
            if not pn532.mifare_classic_write_block(block, bytearray(splitted_cardId_list[i], "UTF-8")):
                print("Error during writing! Failed to write on block {0}", block)
                print("Cancelling writing")
                raise Exception('Er is iets mis gegaan. Probeer opnieuw')
    return cardId


def ReadCard(pn532):
    print("Place the card on the Scanner")
    key = openConfig()['Encryptionkey']
    if key:
        while True:
            uid = pn532.read_passive_target()
            if uid is not None:
                print('Found card with UID: {0}'.format(get_decoded_string(uid)))
                encrypted_cardId = ""
                block_list = [40, 41, 42]
                for i in range(0, 3):
                    if not pn532.mifare_classic_authenticate_block(uid, block_list[i], MIFARE_CMD_AUTH_B, key):
                        print("Failed to Authenticate block, reading stopped at block: {0}".format(block_list[i]))
                        raise Exception('Kon kaart niet authentificeren, Probeer opniew')
                    else:
                        block_data = bytearray(pn532.mifare_classic_read_block(block_list[i])).decode("UTF-8")
                        if block_data is not None:
                            encrypted_cardId += block_data
                        else:
                            print("No data to be found on block {0}".format(block_list[i]))
                            raise Exception('Geen data gevonden op kaart')
                print("All blocks are read, decrypting now....")
                encrypted_cardId = encrypted_cardId[0:45]
                decrypted_cardId = AESecryption().decrypt(encrypted_cardId)
                print('==============================================================')
                print('CARD ID FOUND: {0}'.format(decrypted_cardId))
                print('==============================================================')
                return decrypted_cardId
            else:
                continue
    else:
        raise Exception

def SecureCard(pn532):
    DEFAULT_CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    sectory_trailer = 43
    print("Place the card on the writer to start ")
    uid = None
    while uid is None:
        uid = pn532.read_passive_target()
    print("Found card with UID: {0}".format(get_decoded_string(uid)))
    print('==============================================================')
    print('WARNING: DO NOT REMOVE CARD FROM PN532 UNTIL FINISHED WRITING!')
    print('==============================================================')
    if not pn532.mifare_classic_authenticate_block(uid, sectory_trailer, MIFARE_CMD_AUTH_A,
                                                       DEFAULT_CARD_KEY):
        print('Error! Failed to authenticate sector trailer. Try again')
        raise Exception('Kon kaart niet authentificeren. Probeer opnieuw')

    sector_trailer_block = "{0} {1} {2}".format('6B 3D 73 34 4C 29', '70 F0 F8 FF', '75 42 64 35 5f 5d')
    dataArray = bytearray.fromhex(sector_trailer_block)
    if not pn532.mifare_classic_write_block(sectory_trailer, dataArray):
        print('Error! Failed to write the sector trailer')
        raise Exception('Kon kaart niet blokkeren. Probeer opnieuw')
    return True