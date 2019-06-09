from Configure import *
from PL.Windows import *
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
        try:
            while True:
                pkey = keypad.pressed_keys
                if pkey:
                    time.sleep(0.5)
                    if pkey[0] == 1:
                        PaymentWindow(disp, keypad, pn532).show()
                    elif pkey[0] == 2:
                             ww = WriteWindow(disp)
                             ww.show(pn532)
                             sw = SecureWindow(disp)
                             sw.show(pn532, ww.getCardId(), keypad)
                             time.sleep(5)
                             self.showModeWindow(disp)
                    elif pkey[0] == 'C':
                        disp.reset()
                        sys.exit(-1)
                    else:
                        continue
        except Exception as e:
            DisplayError(disp, str(e)).show()
            time.sleep(5)
            self.showModeWindow(disp)
        except KeyboardInterrupt:
            self.showModeWindow(disp)



if __name__ == '__main__':
    Main().Start()