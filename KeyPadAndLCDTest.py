from digitalio import DigitalInOut
import time
import board
from Hardware import adafruit_matrixkeypad
from Hardware.LCDTest import configure
from PIL import ImageDraw, Image, ImageFont

cols = [DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
rows = [DigitalInOut(x) for x in (board.D16, board.D5, board.D13, board.D19)]

keys = [(1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#')]

disp = configure()

disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
print(width, height)
image = Image.new('1', (width, height))


# Make sure to create image with mode
draw = ImageDraw.Draw(image)


# Load default font.
font = ImageFont.load_default()

#draw.text((2, 2), 'Hello World!', font=font, fill=255)

disp.image(image)
disp.display()


x = [128, 64]
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

while True:
    i = 2
    keys = keypad.pressed_keys
    if keys:
        draw.text((i + 10, 2), str(keys[0]), font=font, fill=255)
        print("Pressed: ", keys[0])
        disp.image(image)
        disp.display()
    i += 10
    print(i)
    time.sleep(0.1)
    