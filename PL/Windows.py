from DAL.ApiController import getPINResponse
from PIL import ImageDraw, Image, ImageFont
import time
class ModeWindow:

    def __init__(self, disp):
        self.name = "ModeWindow"
        self.disp = disp
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self.disp.image(self.image)

    def show(self):
        self.disp.clear()
        self.draw.text((10, 10), 'Choose a mode', font=self.font, fill=255)
        self.draw.text((10, 30), '1 | PIN mode', font=self.font, fill=255)
        self.draw.text((10, 50), '2 | Write mode', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

class AmountWindow:

    def __init__(self, display):
        self.disp = display
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self.disp.image(self.image)

    def show(self):
        self.disp.clear()
        self.disp.display()
        self.draw.text((10, 10), 'Enter amount', font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def getAmount(self, keypad):
        self.disp.clear()
        self.disp.display()
        amount = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while True:
            pkey = keypad.pressed_keys
            if pkey:
                print("key pressed " , pkey)
                time.sleep(1)
                if pkey[0] == "#":
                    break
                elif pkey[0] == "C":
                    return None
                elif pkey[0] == "*":
                    amount = amount[:-1]
                    self.disp.clear()
                    self.disp.display()
                    self.image = Image.new('1', (self.disp.width, self.disp.height))
                    self.draw = ImageDraw.Draw(self.image)
                    self.draw.text((50, 30), str(int(amount) / float(100)), font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                elif int(pkey[0]) in numbers:
                    amount += str(pkey[0])
                    self.disp.clear()
                    self.disp.display()
                    self.image = Image.new('1', (self.disp.width, self.disp.height))
                    self.draw = ImageDraw.Draw(self.image)
                    self.draw.text((50, 30), str(int(amount) / float(100)), font=self.font, fill=255)
                    self.disp.image(self.image)
                    self.disp.display()
                else:
                    continue
            else:
                continue
        return float(amount)

class PinWindow:

    def __init__(self, display, amount):
        self.display = display
        self.amount = amount

    def show(self):
        self.display.lcd.clear()
        self.display.lcd.display()
        self.display.draw.text((50, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font, fill=255)
        self.display.draw.text((50, 50), "Uw kaart AUB", font=self.display.font, fill=255)
        self.display.lcd.image(self.display.image)
        self.display.lcd.display()

    def getPin(self, keypad):
        self.display.lcd.clear()
        self.display.lcd.display()
        self.display.draw.text((50, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font, fill=255)
        self.display.draw.text((50, 50), "Uw PIN AUB", font=self.display.font, fill=255)
        self.display.lcd.image(self.display.image)
        self.display.lcd.display()
        pin = ''
        output = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while True:
            pkey = keypad.pressed_keys
            if pkey == ["#"]  and len(output) == 4:
                break
            elif pkey == "C":
                return None
            elif pkey == ["*"]:
                pin = pin[:-1]
                output = output[:-1]
                self.display.lcd.clear()
                self.display.draw.text((50, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font,
                                       fill=255)
                self.display.draw.text((50, 30), "Uw PIN AUB", font=self.display.font, fill=255)
                self.display.draw.text((50, 50), output, font=self.display.font, fill=255)
                self.display.lcd.image(self.display.image)
                self.display.lcd.display()
            elif int(pkey) in numbers:
                pin += pkey
                output = '*'
                output += ' '
                self.display.lcd.clear()
                self.display.draw.text((50, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font,
                                       fill=255)
                self.display.draw.text((50, 30), "Uw PIN AUB", font=self.display.font, fill=255)
                self.display.draw.text((50, 50), output, font=self.display.font, fill=255)
                self.display.lcd.image(self.display.image)
                self.display.lcd.display()
            else:
                continue
        return pin

class ResultWindow:

    def __init__(self, display, amount, pin, cardId):
        self.display = display
        self.amount = amount
        self.pin = pin
        self.cardId = cardId

    def show(self):
        self.display.lcd.clear()
        self.display.lcd.display()
        response = getPINResponse(self.pin, self.cardId, self.amount)
        if response.status_code == "400":
            self.display.lcd.clear()
            self.display.draw.text((50, 30), "Wrong Pin", font=self.display.font, fill=255)
            self.display.lcd.display()
        elif response.status_code == "500":
            self.display.lcd.clear()
            self.display.draw.text((50, 30), "Not enough Saldo", font=self.display.font, fill=255)
            self.display.lcd.display()
        elif response.status_code == "600":
            self.display.lcd.clear()
            self.display.draw.text((50, 30), "OK", font=self.display.font, fill=255)
            self.display.lcd.display()
        else:
            print("Unexpected response")



