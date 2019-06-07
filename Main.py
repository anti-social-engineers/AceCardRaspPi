from Configure import *
from PIL import ImageDraw, Image, ImageFont
from BLL.Display import Display
from PL.Windows import *
from DAL.NfcController.Read import ReadCard
import time
import sys

class Main:

    def Start(self):

        pn532 = PN532().initialize()
        keypad = MatrixKeyPad().initialize()
        lcd = SSD106().initialize()

        lcd.begin()
        image = Image.new('1', (lcd.width, lcd.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        #Creating instance so i can pass this to all windows
        display = Display(lcd, draw, image, font)
        #draw.text((10, 10), "Choose a mode to use ", font=font, fill=255)

        lcd.image(image)
        lcd.display()

        self.ToMain(display)
        self.mainLoop(display, keypad, pn532)

    def ToMain(self, display):
        mode = ModeWindow(display)
        mode.show()


    def mainLoop(self, display, keypad, pn532):

        while True:
            pkey = keypad.pressed_keys
            if pkey:
                print("key pressed", pkey)
                if pkey == [1]:
                    print("enter mode 1")
                    amountWindow = AmountWindow(display)
                    amountWindow.show()
                    amount = amountWindow.getAmount(keypad)
                    print(amount)
                    if amount is not None:
                        pinWindow = PinWindow(display, amount)
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
                                self.ToMain(display)
                    else:
                        self.ToMain(display)
            else:
                continue







if __name__ == '__main__':
    Main().Start()