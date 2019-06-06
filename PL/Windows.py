class ModeWindow:

    def __init__(self, display):
        self.display = display

    def show(self):
        self.display.lcd.clear()
        self.display.draw.text((10, 10), 'Choose a mode', font=self.display.font, fill=255)
        self.display.draw.text((10, 30), '1 | PIN mode', font=self.display.font, fill=255)
        self.display.draw.text((10, 50), '2 | Write mode', font=self.display.font, fill=255)
        self.display.lcd.display()

class AmountWindow:

    def __init__(self, display):
        self.display = display

    def show(self):
        self.display.lcd.clear()
        self.display.draw.text((10, 10), 'Enter amount', font=self.display.font, fill=255)
        self.display.draw.text((10, 50), "0.00", font=self.display.font, fill=255)
        self.display.lcd.display()

    def getAmount(self, keypad):
        amount = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while True:
            pkey = keypad.pressed_keys[0]
            if pkey == "A":
                break
            elif pkey == "C":
                return None
            elif pkey == "*":
                amount = amount[:-1]
                self.display.lcd.clear()
                self.display.draw.text((10, 10), 'Enter amount', font=self.display.font, fill=255)
                self.display.draw.text((10, 50), str(int(amount) / float(100)), font=self.display.font, fill=255)
                self.display.lcd.display()
            elif int(pkey) in numbers:
                amount += pkey
                self.display.lcd.clear()
                self.display.draw.text((10, 10), 'Enter amount', font=self.display.font, fill=255)
                self.display.draw.text((10, 50), str(int(amount) / float(100)), font=self.display.font, fill=255)
                self.display.lcd.display()
            else:
                continue
        return float(amount)

class PinWindow:

    def __init__(self, display, amount):
        self.display = display
        self.amount = amount

    def show(self):
        self.display.lcd.clear()
        self.display.draw.text((10, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font, fill=255)
        self.display.draw.text((10, 50), "Uw kaart AUB", font=self.display.font, fill=255)
        self.display.lcd.display()

    def getPin(self, keypad):
        self.display.draw.text((10, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font, fill=255)
        self.display.draw.text((10, 50), "Uw PIN AUB", font=self.display.font, fill=255)
        self.display.lcd.display()
        pin = ''
        output = ''
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        while True:
            pkey = keypad.pressed_keys[0]
            if pkey == "A"  and len(output) == 4:
                break
            elif pkey == "C":
                return None
            elif pkey == "*":
                pin = pin[:-1]
                output = output[:-1]
                self.display.lcd.clear()
                self.display.draw.text((10, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font,
                                       fill=255)
                self.display.draw.text((10, 30), "Uw PIN AUB", font=self.display.font, fill=255)
                self.display.draw.text((10, 50), pin, font=self.display.font, fill=255)
                self.display.lcd.display()
            elif int(pkey) in numbers:
                pin += pkey
                output = '*'
                output += ' '
                self.display.lcd.clear()
                self.display.draw.text((10, 10), str.format('TOT {0} EUR', self.amount), font=self.display.font,
                                       fill=255)
                self.display.draw.text((10, 30), "Uw PIN AUB", font=self.display.font, fill=255)
                self.display.draw.text((10, 50), pin, font=self.display.font, fill=255)
                self.display.lcd.display()
            else:
                continue
        return pin

class ResultWindow:

    def __init__(self, display, amount, pin):
        self.display = display
        self.amount = amount
        self.pin = pin


