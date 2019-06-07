from Configure import *
from PIL import ImageDraw, Image, ImageFont
from PL.Windows import *
from DAL.NfcController.Read import ReadCard
import sys

class Main:

    def Start(self):

        pn532 = PN532().initialize()
        keypad = MatrixKeyPad().initialize()
        disp = SSD106().initialize()

        disp.begin()
        disp.clear()
        disp.display()

        self.ToMain(disp)
        self.mainLoop(disp, keypad, pn532)

    def ToMain(self, display):
        mode = ModeWindow(display)
        mode.show()


    def mainLoop(self, disp, keypad, pn532):

        while True:
            pkey = keypad.pressed_keys
            if pkey:
                print("key pressed", pkey)
                if pkey == [1]:
                    print("enter mode 1")
                    amountWindow = AmountWindow(disp)
                    amountWindow.show()
                    amount = amountWindow.getAmount(keypad)
                    print(amount)
                    if amount is not None:
                        pinWindow = PinWindow(disp, amount)
                        pinWindow.show()
                        #CARD_KEY_B = [0x75, 0x42, 0x64, 0x35, 0x5f, 0x5d]
                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                        cardId = ReadCard(key, pn532)
                        if cardId:
                            pin = pinWindow.getPin(keypad)
                            if pin is not None:
                                sys.exit(-1)
                                # resultWindow = ResultWindow(display, amount, pin)
                                # resultWindow.show()
                            else:
                                self.ToMain(disp)
                    else:
                        self.ToMain(disp)
            else:
                continue







if __name__ == '__main__':
    Main().Start()