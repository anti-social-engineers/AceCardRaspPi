import busio
import board
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import Adafruit_SSD1306
from Adafruit_matrixkeypad import adafruit_matrixkeypad
from PIL import ImageDraw, Image, ImageFont
import Adafruit_GPIO.SPI as SPI

class getPN532:

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
        # harware reset
        self.reset_pin = DigitalInOut(board.D6)
        # On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
        # wakeup! this means we don't need to do the I2C clock-stretch thing
        self.req_pin = DigitalInOut(board.D12)

    def inititalize(self):
        pn532 = PN532_I2C(self.i2c, debug=False, reset=self.reset_pin, req=self.req_pin)
        pn532.SAM_configuration()
        return pn532


class getSSD106:

    def __init__(self):
        # Raspberry Pi pin configuration:
        self.RST = 24
        # Note the following are only used with SPI:
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

    def inititalize(self):
        return Adafruit_SSD1306.SSD1306_128_64(rst=self.RST, dc=self.DC, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000))

class getMatrixKeyPad:

    def __init__(self):
        self.cols = [DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
        self.rows = [DigitalInOut(x) for x in (board.D16, board.D5, board.D13, board.D19)]
        self.keys = [(1, 2, 3),
                     (4, 5, 6),
                     (7, 8, 9),
                   ('*', 0, '#')]

    def initalize(self):
        return adafruit_matrixkeypad.Matrix_Keypad(self.rows, self.cols, self.keys)
