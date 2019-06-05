from digitalio import DigitalInOut
import time
import board
from Hardware import adafruit_matrixkeypad

cols = [DigitalInOut(x) for x in (board.D9, board.D6, board.D5)]
rows = [DigitalInOut(x) for x in (board.D13, board.D12, board.D11, board.D10)]

keys = [(1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#')]

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
    time.sleep(0.1)