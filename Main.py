from Configure import *
from PL.Windows import *
from BLL.CustomErrors import *
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
        time.sleep(2)
        self.mainLoop(disp, keypad, pn532)

    def showModeWindow(self, display):
        ModeWindow(display).show()

    def mainLoop(self, disp, keypad, pn532):
        self.showModeWindow(disp)
        while True:
            try:
                pkey = keypad.pressed_keys
                if pkey:
                    time.sleep(0.5)
                    if pkey[0] == 1:
                        PaymentWindow(disp, keypad, pn532).show()
                        time.sleep(5)
                        self.showModeWindow(disp)
                    elif pkey[0] == 2:
                         ww = WriteWindow(disp)
                         ww.show(pn532)
                         sw = SecureWindow(disp)
                         sw.show(pn532, ww.getCardId(), keypad)
                         time.sleep(2)
                         self.showModeWindow(disp)
                    else:
                         continue
            except UserError as e:
                DisplayError(disp, str(e)).show()
                time.sleep(5)
                self.showModeWindow(disp)
            except NFCScanError as e:
                print(str(e))
                self.showModeWindow(disp)
            except CancelError:
                self.showModeWindow(disp)
            except ApiError as e:
                print(str(e))
                self.showModeWindow(disp)



if __name__ == '__main__':
    Main().Start()