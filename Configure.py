import busio
import board
import Adafruit_GPIO.SPI as SPI
from digitalio import DigitalInOut
from Libraries.Adafruit_pn532.i2c import PN532_I2C
from Libraries import Adafruit_SSD1306
from Libraries.Adafruit_matrixkeypad import adafruit_matrixkeypad


class PN532:

    """
    Configuring of the PN532. We configure the pins that are connected to the Pi. And initialize the library
    """
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
        # harware reset
        self.reset_pin = DigitalInOut(board.D6)
        # On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
        # wakeup! this means we don't need to do the I2C clock-stretch thing
        self.req_pin = DigitalInOut(board.D12)

    def initialize(self):
        print("initializing pn532")
        pn532 = PN532_I2C(self.i2c, debug=False, reset=self.reset_pin, req=self.req_pin)
        pn532.SAM_configuration()
        print("firmware version: {0} ".format(pn532.get_firmware_version()))
        return pn532


class SSD106:
    """
    Configuring of the LCD. We configure the pins that are connected to the Pi. And initialize the library
    """
    def __init__(self):
        # Raspberry Pi pin configuration:
        self.RST = 24
        # Note the following are only used with SPI:
        self.DC = 23
        self.SPI_PORT = 0
        self.SPI_DEVICE = 0

    def initialize(self):
        return Adafruit_SSD1306.SSD1306_128_64(rst=self.RST, dc=self.DC, spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000))

class MatrixKeyPad:
    """
    Configuring of the KeyPad. We configure the pins that are connected to the Pi. And initialize the library
    keys are default keys that are projected on the keypad
    """
    def __init__(self):
        self.cols = [DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
        self.rows = [DigitalInOut(x) for x in (board.D16, board.D5, board.D13, board.D19)]
        self.keys = [(1, 2, 3),
                     (4, 5, 6),
                     (7, 8, 9),
                   ('*', 0, '#')]

    def initialize(self):

        return adafruit_matrixkeypad.Matrix_Keypad(self.rows, self.cols, self.keys)
