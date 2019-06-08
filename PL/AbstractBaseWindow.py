from abc import ABC, abstractmethod
from PIL import ImageDraw, Image, ImageFont

class BaseWindow(ABC):
    def __init__(self, disp):
        self.disp = disp
        self.image = Image.new('1', (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        super(BaseWindow).__init__()

    @abstractmethod
    def show(self):
        pass