from DAL.ApiController import getPINResponse
from PL.AbstractBaseWindow import BaseWindow
from DAL.NfcController import WriteCard, ReadCard, SecureCard
from DAL.ApiController import getToken
import time


class MainWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.drawText(30, 10, 'Welkom bij Ace')
        self.disp.display(0)


class ModeWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.drawText(10, 10, 'Kies modus')
        self.drawText(10, 10, '1 | PIN mode')
        self.drawText(10, 10, '2 | Secure mode')
        self.disp.image(self.image)
        self.disp.display()

class AmountWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.drawText(10, 10, 'Voer bedrag in')
        self.drawText(10, 10, '0.00')
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
                self.drawText(10, 10, 'Voer bedrag in')
                self.drawText(5, 50, '* | Terug')
                self.drawText(100, 50, '# | OK')
                time.sleep(1)
                if pkey[0] == '#':
                    okPressed = True
                elif pkey[0] == '*' and len(amount) > 0:
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
        return float(amount)

class PinWindow(BaseWindow):

    def __init__(self, disp, amount):
        self.amount = amount
        super(BaseWindow).__init__(disp)

    def show(self):

        self.drawText(50, 10, 'TOT {0} EUR'.format(self.amount))
        self.drawText(50, 50, "Uw kaart AUB")
        self.disp.image(self.image)
        self.disp.display()

    def getPin(self, keypad):
        pin = ''
        output = ''
        okPressed = False
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while not okPressed:
            self.newImage()
            self.drawText(50, 10, 'TOT {0} EUR'.format(self.amount))
            self.drawText(50, 50, "Uw PIN AUB")
            self.drawText(5, 50, '* | Terug')
            self.drawText(100, 50, '# | OK')
            pkey = keypad.pressed_keys
            if pkey:
                if pkey[0] == '#':
                    okPressed = True
                elif pkey[0] == "*" and len(pin) > 0:
                    pin = pin[:-1]
                    output = output[:-2]
                    self.drawText(50, 50, output)
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers and len(pin) <= 4:
                    pin += pkey
                    output += '*'
                    output += ' '
                    self.drawText(50, 50, output)
                    self.disp.image(self.image)
                    self.disp.display()
                elif pkey[0] == 'C':
                    raise KeyboardInterrupt('Onderbroken')
                else:
                    continue
        return pin

class PaymentWindow(BaseWindow):

    def __init__(self, disp, keypad, pn532):
        self.keypad = keypad
        self.pn532 = pn532
        super(BaseWindow).__init__(disp)

    def show(self):
        self.disp.clear()
        aw = AmountWindow(self.disp)
        aw.show()
        amount = aw.getAmount(self.keypad)
        pw = PinWindow(self.disp,amount)
        pw.show()
        pin = pw.getPin(self.keypad)
        cardId = ReadCard(self.pn532)
        token = getToken()
        response = getPINResponse(token, amount, pin, cardId)
        while not response.status_code == 201:
            self.newImage()
            animation = ''
            loading = 0
            while response is None:
                self.loading(animation, loading)
            if response.status_code == 400:
                raise Exception('Onvoldoende saldo!')
            elif response.status_code == 401:
                if response.json() == 'Unauthorized':
                    token = getToken()
                    response = getPINResponse(token, amount, pin, cardId)
                else:
                    self.drawText(50, 30, 'Incorrect PIN')
                    pin = pw.getPin(self.keypad)
                    response = getPINResponse(token, amount, pin, cardId)
            elif response.status_code == 429 or response.status_code == 403:
                raise Exception('Kaart is geblokkeerd')
            elif response.status_code == 403:
                raise Exception('Kaart is niet gevonden')
            else:
                raise KeyboardInterrupt
        self.drawText(50, 10, 'TOT {0} EUR'.format(amount))
        self.drawText(50, 30, 'Betaling succes')
        self.disp.image(self.image)
        self.disp.display()

    def loading(self, animation, loading):
        while True:
            if loading > 3:
                loading = 0
                animation = ''
            self.newImage()
            self.drawText(50, 30, 'Laden{0}'.format(animation))
            self.disp.display()
            animation += '.'
            loading += 1


class WriteWindow(BaseWindow):

    def __init__(self, disp):
        self.cardId = None
        super(BaseWindow).__init__(disp)

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
        super(BaseWindow).__init__(disp)

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
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((50, 50), self.result, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()


