import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import ImageDraw, Image, ImageFont

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))


# Make sure to create image with mode
draw = ImageDraw.Draw(image)


# Load default font.
font = ImageFont.load_default()

draw.text((2, 2), 'Hello World!', font=font, fill=255)

disp.image(image)
disp.display()