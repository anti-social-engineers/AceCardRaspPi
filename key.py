CARD_KEY_A = [0x6B, 0x3D, 0x73, 0x34, 0x4C, 0x29]
CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]

CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

def getkey():
    choice = input("which key? a/b/d(default)")
    if choice.lower() == "a":
        return CARD_KEY_A
    elif choice.lower() == "b":
        return CARD_KEY_B
    elif choice.lower() == "d":
        return CARD_KEY
    return CARD_KEY


