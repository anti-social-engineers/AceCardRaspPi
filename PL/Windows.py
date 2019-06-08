from DAL.ApiController import getPINResponse
from PIL import ImageDraw, Image
from PL.AbstractBaseWindow import BaseWindow
import time


class MainWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((30, 10), 'Welkom bij Ace', font=self.font, fill=255)
        self.disp.display(0)


class ModeWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((10, 10), 'Kies modus', font=self.font, fill=255)
        self.draw.text((10, 30), '1 | PIN mode', font=self.font, fill=255)
        self.draw.text((10, 50), '2 | Write mode', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

class AmountWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((10, 10), 'Enter bedrag', font=self.font, fill=255)
        self.draw.text((50, 30), '0.00', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def getAmount(self, keypad):
        amount = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        okPressed = False
        while not okPressed:
            pkey = keypad.pressed_keys
            if pkey:
                self.image = Image.new('1', (self.disp.width, self.disp.height))
                self.draw = ImageDraw.Draw(self.image)
                self.draw.text((10, 10), 'Voer bedrag in', font=self.font, fill=255)
                self.draw.text((5, 50), '* | Terug', font=self.font, fill=255)
                self.draw.text((100, 50), '# | OK', font=self.font, fill=255)
                time.sleep(1)
                if pkey[0] == "#":
                    okPressed = True
                elif pkey[0] == "C":
                    return None
                elif pkey[0] == "*" and len(amount) > 0:
                    self.draw.text((50, 30), str(int(amount) / float(100)), font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers:
                    amount += str(pkey[0])
                    self.draw.text((50, 30), str(int(amount) / float(100)), font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                else:
                    continue
        return float(amount)

class PinWindow(BaseWindow):

    def __init__(self, disp, amount):
        self.amount = amount
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((50, 10), 'TOT {0} EUR'.format(self.amount), font=self.font, fill=255)
        self.draw.text((50, 50), "Uw kaart AUB", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def getPin(self, keypad):
        pin = ''
        output = ''
        okPressed = False
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while not okPressed:
            self.image = Image.new('1', (self.disp.width, self.disp.height))
            self.draw = ImageDraw.Draw(self.image)
            self.draw.text((50, 10), 'TOT {0} EUR'.format(self.amount), font=self.font, fill=255)
            self.draw.text((50, 50), "Uw PIN AUB", font=self.font, fill=255)
            self.draw.text((5, 50), '* | Terug', font=self.font, fill=255)
            self.draw.text((100, 50), '# | OK', font=self.font, fill=255)
            pkey = keypad.pressed_keys
            if pkey:
                if pkey[0] == "#":
                    okPressed = True
                elif pkey[0] == "C":
                    return None
                elif pkey[0] == "*" and len(pin) > 0:
                    pin = pin[:-1]
                    output = output[:-1]
                    self.draw.text((50, 50), output, font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers and len(pin) <= 4:
                    pin += pkey
                    output += '*'
                    self.draw.text((50, 50), output, font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                else:
                    continue
        return pin

class ResultWindow(BaseWindow):

    def __init__(self, disp, amount, pin, cardId):
        self.amount = amount
        self.pin = pin
        self.cardId = cardId
        super(BaseWindow).__init__(disp)

    def show(self):
        response = getPINResponse(self.amount, self.pin, self.cardId)
        self.draw.text((50, 50), str(response.status_code), font=self.font, fill=255)
        self.disp.display()


class WriteWindow(BaseWindow):

    def __init__(self, disp):
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((50, 10), 'Plaats the kaart op de scanner', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def confirmBlock(self):
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)


class SecureWindow(BaseWindow):

    def __init__(self, disp, cardId):
        self.cardId = cardId
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((50, 10), 'Kaart geschreven met Id: {0}'.format(self.cardId), font=self.font, fill=255)
        self.draw.text((5, 50), '* | NO', font=self.font, fill=255)
        self.draw.text((100, 50), '# | YES', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()


    def confirmBlock(self, keyPad):
        okPressed = False
        while not okPressed:
            pkey = keyPad.pressed_keys
            if pkey:
                time.sleep(0.5)
                if pkey[0] ==  '*':
                    return False
                elif pkey[0] == '#':
                    return True
                elif pkey[0] == "C":
                    return None
                else:
                    continue
            else:
                continue

class OutputWindow(BaseWindow):

    def __init__(self, disp, result):
        self.result = result
        super(BaseWindow).__init__(disp)

    def show(self):
        self.draw.text((50, 50), self.result, font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()


