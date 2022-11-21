# Constants.py
OLED_RES_X = 128  # SSD1306 horizontal resolution
OLED_RES_Y = 64   # SSD1306 vertical resolution


# Player.py
import framebuf


class Player:
    def __init__(self, oled):
        self.width = 9
        self.height = 10
        self.__img = bytearray(
            b'\x08\x00\x1c\x00\x14\x00\x14\x00\x1c\x00>\x00\x7f\x00\xff\x80\xdd\x80\x08\x00')
        self.__fb = framebuf.FrameBuffer(
            self.__img, self.width, self.height, framebuf.MONO_HLSB)  # MONO_HLSB
        self.X = 0
        self.Y = 54
        self.oled = oled

    def render_player(self):
        # show the image at location (x=X,y=Y)
        self.oled.blit(self.__fb, self.X, self.Y)

    def move_left(self):
        if self.X > 0:
            self.X -= 1

    def move_right(self):
        if self.X < OLED_RES_X - self.width:
            self.X += 1

    def move_up(self):
        half_screen = OLED_RES_Y // 2 - self.height
        if self.Y > half_screen:
            self.Y -= 1

    def move_down(self):
        if self.Y < OLED_RES_Y - self.height:
            self.Y += 1

# frame buff types: GS2_HMSB, GS4_HMSB, GS8, MONO_HLSB, MONO_VLSB, MONO_HMSB, MVLSB, RGB565


# Main.py
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C

if __name__ == '__main__':
    # start I2C on I2C1 (GPIO 26/27)
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
    oled = SSD1306_I2C(OLED_RES_X, OLED_RES_Y, i2c)  # oled controller

    xAxis = ADC(Pin(27))
    yAxis = ADC(Pin(26))
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    player = Player(oled)
    x = 0
    while True:
        oled.fill(0)  # clear the OLED
        player.render_player()
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
        buttonValue = button.value()
        buttonStatus = "not pressed"
        if xValue <= 600:
            player.move_left()
            # "left"
        elif xValue >= 60000:
            player.move_right()
            # "right"
        if yValue <= 600:
            player.move_up()
            # "up"
        elif yValue >= 60000:
            player.move_down()
            # "down"
        if buttonValue == 0:
            buttonStatus = "pressed"
        oled.show()


