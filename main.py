from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import sys


pix_res_x = 128  # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution

# start I2C on I2C1 (GPIO 26/27)
i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)  # oled controller


class Player:
    def __init__(self):
        self.width = 9
        self.height = 10
        self.__img = bytearray(
            b'\x08\x00\x1c\x00\x14\x00\x14\x00\x1c\x00>\x00\x7f\x00\xff\x80\xdd\x80\x08\x00')
        self.__fb = framebuf.FrameBuffer(
            self.__img, self.width, self.height, framebuf.MONO_HLSB)  # MONO_HLSB
        self.X = 0
        self.Y = 54

    def render_player(self):
        # show the image at location (x=X,y=Y)
        oled.blit(self.__fb, self.X, self.Y)

    def move_left(self):
        self.X -= 1

    def move_right(self):
        self.X += 1


# frame buff types: GS2_HMSB, GS4_HMSB, GS8, MONO_HLSB, MONO_VLSB, MONO_HMSB, MVLSB, RGB565


player = Player()
x = 0
while True:
    oled.fill(0)  # clear the OLED
    player.render_player()

    oled.show()
