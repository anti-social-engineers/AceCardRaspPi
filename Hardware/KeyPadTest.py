from digitalio import DigitalInOut
import time
import board
import adafruit_matrixkeypad

cols = [DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
rows = [DigitalInOut(x) for x in (board.D16, board.D5, board.D13, board.D19)]

keys = [(1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#')]

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)




def pressedKey():
    while True:
        keys = keypad.pressed_keys
        if keys:
            print(keys[0])
            time.sleep(0.5)


if __name__ == '__main__':
    pressedKey()


