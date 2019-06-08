from Configure import *
from PL.Windows import *
from DAL.NfcController.Read import ReadCard
from DAL.NfcController.Write import WriteCard
from DAL.NfcController.Block import SecureCard
import sys


class Main:

    def Start(self):

        pn532 = PN532().initialize()
        keypad = MatrixKeyPad().initialize()
        disp = SSD106().initialize()

        disp.begin()
        disp.clear()
        disp.display()

        MainWindow(disp).show()
        time.sleep(3)
        self.mainLoop(disp, keypad, pn532)

    def showModeWindow(self, display):
        mode = ModeWindow(display)
        mode.show()

    def mainLoop(self, disp, keypad, pn532):
        self.showModeWindow(disp)
        while True:
            pkey = keypad.pressed_keys
            if pkey:
                time.sleep(0.5)
                if pkey[0] == 1:
                    amountWindow = AmountWindow(disp)
                    amountWindow.show()
                    amount = amountWindow.getAmount(keypad)
                    if amount is not None:
                        paymentSucces = False
                        while not paymentSucces:
                            pinWindow = PinWindow(disp, amount)
                            pinWindow.show()
                            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                            cardId = ReadCard(key, pn532)
                            if cardId:
                                pin = pinWindow.getPin(keypad)
                                if pin is not None:
                                    ResultWindow(disp, amount, pin, cardId).show()
                                    time.sleep(5)
                                    paymentSucces = True
                                else:
                                    self.showModeWindow(disp)
                            else:
                                self.showModeWindow(disp)
                        self.showModeWindow(disp)
                elif pkey[0] == 2:
                     WriteWindow(disp).show()
                     try:
                         cardId = WriteCard(pn532)
                         secureWindow = SecureWindow(disp, cardId)
                         secureWindow.show()
                         if SecureCard(pn532, secureWindow.confirmBlock(keypad)):
                             OutputWindow(disp, 'Het is veilig om de kaart te verwijderen van de scanner').show()
                             time.sleep(3)
                             self.showModeWindow(disp)
                         else:
                             time.sleep(3)
                             self.showModeWindow(disp)
                     except Exception as e:
                         OutputWindow(disp, str(e)).show()
                         time.sleep(5)
                         self.showModeWindow(disp)
                elif pkey[0] == 'C':
                    disp.reset()
                    sys.exit(-1)



            else:
                continue


if __name__ == '__main__':
    Main().Start()