from Configure import *
from PIL import ImageDraw, Image, ImageFont
import time



def main():

    pn532 = getPN532().inititalize()
    keypad = getMatrixKeyPad().initalize()
    display = getSSD106().inititalize()

    display.begin()
    display.clear()
    display.display()
    image = Image.new('1', (display.width, display.height))
    # Make sure to create image with mode
    draw = ImageDraw.Draw(image)

    # Load default font.
    font = ImageFont.load_default()

    draw.text((10, 10), "Choose a mode to use ", font=font, fill=255)
    draw.text((10, 25), "--------------------------------", font=font, fill=255)
    draw.text((10, 40), "1 | PIN Mode", font=font, fill=255)
    draw.text((10, 55), "2 | Write and Secure Mode", font=font, fill=255)

    display.image(image)
    display.display()

    while True:
        pkey = keypad.pressed_keys[0]
        if pkey:
            if pkey[0] == "1":
                draw.text((10, 40), "1 | PIN Mode", font=font, fill=255)
            elif pkey[0] == "2":

            else:
                continue






if __name__ == '__main__':
    main()