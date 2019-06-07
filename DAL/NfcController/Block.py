from BLL.Logic import *
from Libraries.Adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from DAL.NfcController.Read import ReadCard


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
    ReadCard(DEFAULT_CARD_KEY, pn532)
    choice = input("Are you sure you want to secure sector 10? This means the acces bits will be overwritten and a different key must be used to read the card!!!! (Y/N)?")
    if choice.lower() == "y":
        if not pn532.mifare_classic_authenticate_block(uid, sectory_trailer, MIFARE_CMD_AUTH_A,
                                                       DEFAULT_CARD_KEY):
            print('Error! Failed to authenticate sector trailer. Try again')
            sys.exit(-1)
        sector_trailer_block = "{0} {1} {2}".format('6B 3D 73 34 4C 29', '70 F0 F8 FF', '75 42 64 35 5f 5d')
        dataArray = bytearray.fromhex(sector_trailer_block)
        if not pn532.mifare_classic_write_block(sectory_trailer, dataArray):
            print('Error! Failed to write the sector trailer')
            sys.exit(-1)
        print("Acces bits have been overwritten")
    else:
        print("Writing has been cancelled!")
        sys.exit(-1)



