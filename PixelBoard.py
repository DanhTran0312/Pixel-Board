import time
import neopixel
import random
from imageio import imread


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

class PixelBoard():
    def __init__(self,pin, heigth, width, brightness):
        self.pin = pin
        self.height = heigth
        self.width = width
        self.brightness = brightness
        self.n = self.width * self.height
        self.neopixel = neopixel.NeoPixel(self.pin, self.height*self.width, brightness = self.brightness, auto_write =False)


    def clear(self):
        self.neopixel.fill((0,0,0))
        self.show()


    def fillRow(self, row, color):
        for i in range(self.width):
            self.setColor((row, i), color)


    def fillCol(self, col, color):
        for i in range(self.height):
            self.setColor((i, col), color)


    def show(self):
        self.neopixel.show()


    def runningLight(self, n, color, delay):
        self.clear()
        for i in range(n,self.n):
            for j in range (n):
                self.neopixel[i-j] = color
            self.show()
            time.sleep(delay)
            self.clear()


    def cyloneCol(self, col,  n, color, delay):
        self.clear()
        for i in range(n,self.height):
            for j in range(n):
                self.setColor((i-j,col), color)
            self.show()
            time.sleep(delay)
            self.clear()

        for i in reversed(range(self.height-n)):
            for j in range(n):
                self.setColor((i+j,col), color)
            self.show()
            time.sleep(delay)
            self.clear()



    def cyloneRow(self, row,  n, color, delay):
        self.clear()
        for i in range(n,self.width):
            for j in range(n):
                self.setColor((row,i-j), color)
            self.show()
            time.sleep(delay)
            self.clear()

        for i in reversed(range(self.width-n)):
            for j in range(n):
                self.setColor((row,i+j), color)
            self.show()
            time.sleep(delay)
            self.clear()


    def displayImage(self, image):
        for row in range(self.height):
            for col in range(self.width):
                self.setColor((col,row), tuple(image[f'{col}, {row}']))
        self.show()


    def cyloneColN(self, col,  n, color, delay, time):
        for i in range(time):
            self.cyloneCol(col,  n, color, delay)


    def cyloneRowN(self, row,  n, color, delay, time):
        for i in range(time):
            self.cyloneCol(row,  n, color, delay)



    def setColor(self, pos, color):
        x = pos[0]
        y = pos[1]
        index = 0
        if(x % 2 == 0):
            index = (self.height - x) * self.width - y - 1
        else:
            index = (self.height - x) * self.width - (self.width - y)
        self.neopixel[index] = color


    def rainbow_cycle(self,wait):
        for j in range(255):
            for i in range(self.n):
                pixel_index = ((255-i) * 256 // self.n) + j
                self.neopixel[255-i] = wheel(pixel_index & 255)
            self.neopixel.show()
            time.sleep(wait)
