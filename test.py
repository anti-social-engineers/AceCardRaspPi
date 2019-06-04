# from Logic import *
# from Encryption import *
import json
import requests
from Logic import *
from DAL.ApiController import *

#
#
# duid = "abcd1234"
# temp_key = "C*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeS"
# cardId = generateUid(duid)
# print(cardId)
# encrypted_cardId = AESecryption(temp_key).encrypt(cardId) + "0000"
#
#
# print(encrypted_cardId)
# splitted_cardId_list = split_encrypted_into_blocks(encrypted_cardId)
#
# print(splitted_cardId_list)
#
#
# block_list = [40, 41, 42]
# print("Starting to write all blocks")
# for i in range(0, 3):
#     block = block_list[i]
#     print(block, bytearray(splitted_cardId_list[i], "UTF-8  "))
#
#
#
#
#
# # CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
# # CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]
# #
# # CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
# #
# # test = bytearray(CARD_KEY_A + [0x08, 0x77, 0x8F, 0xFF] + CARD_KEY_B).hex()
# # s = " ".join(test[i:i+2] for i in range(0, len(test), 2))
# #
# #
# CARD_KEY_A = '6B 3D 73 34 4C 29'
# CARD_KEY_B = '75 42 64 35 5f 5d'
# accessbits = '70 F0 F8 FF'
# sector_trailer_block = "{0} {1} {2}".format(CARD_KEY_A, accessbits, CARD_KEY_B)
# print(sector_trailer_block)
#
#
# # print('6B 3D 73 34 4C 29 08 77 8F FF 75 42 64 35 5f 5d' == f)
# # print(test)
# # print(s)
#
#
# print("Changes to commit")
#
# CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
# CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]
#
# CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
#

# writejson()
# login()

print(getToken())