from abc import ABC
from PIL import ImageDraw, Image, ImageFont

class BaseWindow(ABC):
    def __init__(self, disp):
        self.disp = disp
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        self.disp.clear()
        self.disp.display()

    def drawText(self, x, y, text):
        self.draw.text((x, y), text, font=self.font, fill=255)

    def newImage(self):
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)

    def Display(self):
        self.disp.image(self.image)
        self.disp.display()