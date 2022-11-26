# Constants.py
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C, ADC
import utime
import framebuf
import random
OLED_RES_X = 128  # SSD1306 horizontal resolution
OLED_RES_Y = 64   # SSD1306 vertical resolution
ENEMY_MOVEMENT_THRESHOLD = 20

# Player.py


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
        self.bullets = []
        self.enemies = []

    def render_player(self):
        # show the image at location (x=X,y=Y)
        self.oled.blit(self.__fb, self.X, self.Y)
        for bul in self.bullets:
            self.oled.blit(bul.__fb, bul.X, bul.Y)
        for enem in self.enemies:
            enem.render_enemy()

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

    def handle_bullets(self):
        for bul in self.bullets:
            bul.Y -= 1

            if bul.Y < 0:
                self.bullets.remove(bul)
            for enem in self.enemies:
                if isCollide(bullet=bul, enemy=enem):
                    self.bullets.remove(bul)
                    self.enemies.remove(enem)

    def fire(self):
        self.bullets.append(Bullet(player, oled))


class Bullet:
    def __init__(self, player: Player, oled):
        self.width = 1
        self.height = 3
        self.__img = bytearray(
            b'\x80\x80\x80\x80\x80\x80')
        self.__fb = framebuf.FrameBuffer(
            self.__img, self.width, self.height, framebuf.MONO_HLSB)
        self.X = player.X + player.width // 2
        self.Y = player.Y - player.height // 2


class Enemy:
    def __init__(self, oled) -> None:
        self.width = 11
        self.height = 8
        self.__img = bytearray(
            b' \x80\x1f\x00?\x80n\xc0\xff\xe0\xbf\xa0\xa0\xa0\x1b\x00')
        self.__fb = framebuf.FrameBuffer(
            self.__img, self.width, self.height, framebuf.MONO_HLSB)
        self.X = random.randint(0 + self.width, OLED_RES_X - self.width)
        self.Y = 0
        self.oled = oled

    def render_enemy(self):
        self.oled.blit(self.__fb, self.X, self.Y)

    def move(self):
        self.Y += 1


def draw_win():
    oled.fill(0)  # clear the OLED
    player.render_player()
    oled.show()


def isCollide(enemy: Enemy, bullet: Bullet):
    return (enemy.Y + enemy.height // 2) >= bullet.Y + (bullet.height // 2) and enemy.X - enemy.width // 2 <= bullet.X <= enemy.X + enemy.width

    # frame buff types: GS2_HMSB, GS4_HMSB, GS8, MONO_HLSB, MONO_VLSB, MONO_HMSB, MVLSB, RGB565
last_time = 0  # the last time we pressed the button
button_presses = 0


# Main.py
if __name__ == '__main__':

    def button1_pressed(pin):
        global button_presses, last_time
        new_time = utime.ticks_ms()
        # if it has been more that 1/5 of a second since the last event, we have a new event
        if (new_time - last_time) > 200:
            button_presses += 1
            last_time = new_time

    # start I2C on I2C1 (GPIO 26/27)
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
    oled = SSD1306_I2C(OLED_RES_X, OLED_RES_Y, i2c)  # oled controller

    xAxis = ADC(Pin(27))
    yAxis = ADC(Pin(26))
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(handler=button1_pressed, trigger=Pin.IRQ_RISING)

    player = Player(oled)
    old_presses = 0
    move_enemy = 0

    player.enemies = [Enemy(oled), Enemy(oled)]
    while True:
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
        if button_presses != old_presses:
            old_presses = button_presses
            player.fire()

        move_enemy += 1
        if move_enemy > ENEMY_MOVEMENT_THRESHOLD:
            move_enemy = 0
            for enemy in player.enemies:
                enemy.move()

        draw_win()
        player.handle_bullets()
