from DAL.ApiController import getPINResponse
from PL.AbstractBaseWindow import BaseWindow
from DAL.NfcController import WriteCard, ReadCard, SecureCard
from DAL.ApiController import getToken
from BLL.CustomErrors import *
import time


class MainWindow(BaseWindow):

    def __init__(self, disp):
        super().__init__(disp)

    def show(self):
        self.drawText(30, 10, 'Welkom bij Ace')
        self.disp.image(self.image)
        self.disp.display()


class ModeWindow(BaseWindow):

    def __init__(self, disp):
        super().__init__(disp)

    def show(self):
        self.drawText(30, 10, 'Kies modus')
        self.drawText(30, 30, '1 | PIN mode')
        self.drawText(30, 50, '2 | Secure mode')
        self.disp.image(self.image)
        self.disp.display()

class AmountWindow(BaseWindow):

    def __init__(self, disp):
        super().__init__(disp)

    def show(self):
        self.drawText(30, 10, 'Voer bedrag in')
        self.drawText(50, 30, '0.00')
        self.disp.image(self.image)
        self.disp.display()

    def getAmount(self, keypad):
        amount = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        okPressed = False
        while not okPressed:
            pkey = keypad.pressed_keys
            if pkey:
                self.newImage()
                self.drawText(30, 10, 'Voer bedrag in')
                self.drawText(5, 50, '* | Terug')
                self.drawText(80, 50, '# | OK')
                time.sleep(0.5)
                if pkey[0] == '#':
                    okPressed = True
                elif pkey[0] == '*' and len(amount) > 0:
                    amount = amount[:-1]
                    self.drawText(50, 30, str(int(amount) / float(100)))
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers:
                    amount += str(pkey[0])
                    self.drawText(50, 30, str(int(amount) / float(100)))
                    self.disp.image(self.image)
                    self.disp.display()
                elif pkey[0] == 'C':
                    raise KeyboardInterrupt
                else:
                    continue
        return float(int(amount)/float(100))

class PinWindow(BaseWindow):

    def __init__(self, disp, amount):
        self.amount = amount
        super().__init__(disp)

    def show(self):
        self.drawText(30, 10, 'TOT {0} EUR'.format(self.amount))
        self.drawText(30, 30, "Uw kaart AUB")
        self.disp.image(self.image)
        self.disp.display()

    def getPin(self, keypad):
        self.newImage()
        self.drawText(30, 10, 'TOT {0} EUR'.format(self.amount))
        self.drawText(30, 30, "Uw PIN AUB")
        self.disp.image(self.image)
        self.disp.display()
        time.sleep(1)
        pin = ''
        output = ''
        okPressed = False
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while not okPressed:
            self.newImage()
            self.drawText(30, 10, 'TOT {0} EUR'.format(self.amount))
            self.drawText(5, 50, '* | Terug')
            self.drawText(80, 50, '# | OK')
            pkey = keypad.pressed_keys
            if pkey:
                time.sleep(0.5)
                if pkey[0] == '#':
                    okPressed = True
                elif pkey[0] == "*" and len(pin) > 0:
                    pin = pin[:-1]
                    output = output[:-2]
                    self.drawText(40, 30, output)
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers and len(pin) < 4:
                    pin += str(pkey[0])
                    output += '*'
                    output += ' '
                    self.drawText(40, 30, output)
                    self.disp.image(self.image)
                    self.disp.display()
                elif pkey[0] == 'C':
                    raise CancelError
                else:
                    continue
        return pin

class PaymentWindow(BaseWindow):

    def __init__(self, disp, keypad, pn532):
        self.keypad = keypad
        self.pn532 = pn532
        super().__init__(disp)

    def show(self):
        aw = AmountWindow(self.disp)
        aw.show()
        amount = aw.getAmount(self.keypad)
        # cardId = ReadCard(self.pn532)
        pw = PinWindow(self.disp, amount)
        pw.show()
        cardId = '/aetHCBPxhfa2ZMab6hPKxITPqV4ALTqX9ykwZLfbis=0000'
        if cardId is not None:
            print("passed condition cardId")
            pin = pw.getPin(self.keypad)
            token = getToken()
            response = getPINResponse(token, amount, pin, cardId)
            while not response.status_code == 201:
                self.newImage()
                self.drawText(30, 10, 'TOT {0} EUR'.format(amount))
                # animation = ''
                # loading = 0
                # self.loading(response, animation, loading)
                if response.status_code == 401:
                    if response.text == 'Unauthorized':
                        token = getToken()
                        response = getPINResponse(token, amount, pin, cardId)
                    else:
                        self.drawText(30, 30, 'Incorrect PIN.')
                        self.disp.image(self.image)
                        self.disp.display()
                        time.sleep(1)
                        pin = pw.getPin(self.keypad)
                        response = getPINResponse(token, amount, pin, cardId)
                elif response.status_code == 404:
                    self.drawText(30, 30, 'Kaart is niet herkend')
                    self.disp.image(self.image)
                    self.disp.display()
                    time.sleep(1)
                    cardId = ReadCard(self.pn532)
                    pin = pw.getPin(self.keypad)
                    response = getPINResponse(token, amount, pin, cardId)
                elif response.status_code == 429 or response.status_code == 403:
                    raise UserError('Kaart is geblokkeerd.')
                elif response.status_code == 400:
                    raise UserError('Onvoldoende Saldo.')
                elif response.status_code == 403:
                    raise UserError('Toegang geweigerd.')
                else:
                    raise CancelError
            self.drawText(30, 10, 'TOT {0} EUR'.format(amount))
            self.drawText(40, 30, 'AKKOORD')
            self.disp.image(self.image)
            self.disp.display()
        else:
            raise NFCScanError

    def loading(self, response, animation, loading):
        while response is None:
            if loading > 3:
                loading = 0
                animation = ''
            self.newImage()
            self.drawText(50, 30, 'Een ogenblik AUB{0}'.format(animation))
            self.disp.display()
            animation += '.'
            loading += 1


class WriteWindow(BaseWindow):

    def __init__(self, disp):
        self.cardId = None
        super().__init__(disp)

    def show(self, pn532):
        self.drawText(50, 10, 'Plaats the kaart op de scanner')
        self.disp.image(self.image)
        self.disp.display()
        self.cardId = WriteCard(pn532)
        if self.cardId:
            self.newImage()
            self.drawText(50, 10, 'Kaart geschreven met Id:')
            self.drawText(50, 30, '{0}'.format(self.cardId))
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(3)

    def getCardId(self):
        return self.cardId



class SecureWindow(BaseWindow):

    def __init__(self, disp):
        super().__init__(disp)

    def show(self, pn532, cardId, keypad):
        self.drawText(50, 10, 'Kaart geschreven met Id: {}')
        self.drawText(50, 20, 'Wilt u de kaart met Id {0} beveiligen?'.format(cardId))
        self.drawText(50, 30, '{0}'.format(cardId))
        self.drawText(5, 50, '* | NO')
        self.drawText(100, 50, '# | YES')
        self.disp.image(self.image)
        self.disp.display()
        self.confirmBlock(keypad, pn532)

    def confirmBlock(self, keyPad, pn532):
        while True:
            self.newImage()
            pkey = keyPad.pressed_keys
            if pkey:
                time.sleep(0.5)
                if pkey[0] == '#':
                    SecureCard(pn532)
                    self.drawText(10, 10, 'Sector sector overschreven. Verwijder kaart van scanner')
                    self.disp.image(self.image)
                    self.disp.display()
                elif pkey[0] ==  '*':
                    self.drawText(10, 10, 'Kaart beveiliging onderbroken')
                    self.disp.image(self.image)
                    self.disp.display()
                elif pkey[0] == "C":
                    raise KeyboardInterrupt
                else:
                    continue
            else:
                continue

class DisplayError(BaseWindow):

    def __init__(self, disp, result):
        self.result = result
        super().__init__(disp)

    def show(self):
        self.draw.text((30, 30), self.result, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()


