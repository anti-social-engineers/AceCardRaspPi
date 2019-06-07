from BLL.Logic import *
from DAL.Encryption import *

from Libraries.Adafruit_pn532.adafruit_pn532 import *

def ReadCard(key, pn532):
    print("Place the card on the Scanner")
    while True:
        uid = pn532.read_passive_target()
        if uid is not None:
            print('Found card with UID: {0}'.format(get_decoded_string(uid)))
            encrypted_cardId = ""
            block_list = [40, 41, 42]
            for i in range(0, 3):
                if not pn532.mifare_classic_authenticate_block(uid, block_list[i], MIFARE_CMD_AUTH_B, key):
                    print("Failed to Authenticate block, reading stopped at block: {0}".format(block_list[i]))
                    sys.exit(-1)
                else:
                    block_data = bytearray(pn532.mifare_classic_read_block(block_list[i])).decode("UTF-8")
                    if block_data is not None:
                        encrypted_cardId += block_data
                    else:
                        print("No data to be found on block {0}".format(block_list[i]))
            print("All blocks are read, decrypting now....")
            encrypted_cardId = encrypted_cardId[0:45]
            decrypted_cardId = AESecryption().decrypt(encrypted_cardId)
            print('==============================================================')
            print('CARD ID FOUND: {0}'.format(decrypted_cardId))
            print('==============================================================')
            return decrypted_cardId
        else:
            continue


