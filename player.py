# Player.py
import random
from configs import *
from enemy import Enemy
import framebuf


class Heart:
    def __init__(self, X, Y) -> None:
        self.width = 8
        self.height = 8
        self.img = bytearray(b'B\xe7\xff\xff\xff~<\x18')
        self.fb = framebuf.FrameBuffer(
            self.img, self.width, self.height, framebuf.MONO_HLSB
        )
        self.X = X
        self.Y = Y


class Player:
    def __init__(self, oled):
        self.width = 9
        self.height = 10
        self.img = bytearray(
            b'\x08\x00\x1c\x00\x14\x00\x14\x00\x1c\x00>\x00\x7f\x00\xff\x80\xdd\x80\x08\x00')
        self.fb = framebuf.FrameBuffer(
            self.img, self.width, self.height, framebuf.MONO_HLSB)  # MONO_HLSB
        self.X = 0
        self.Y = 54
        self.oled = oled
        self.bullets = []
        self.enemies = []
        self.position = [p * 11 for p in range(11)]  # 11 is width of enemy
        self.score = 0
        self.health = [Heart(i, 0) for i in range(120, 70, -10)]

    def render_player(self):
        # show the image at location (x=X,y=Y)
        self.oled.blit(self.fb, self.X, self.Y)
        for bul in self.bullets:
            self.oled.blit(bul.fb, bul.X, bul.Y)
        for enem in self.enemies:
            enem.render_enemy()

        for enem in self.enemies:
            if enem.Y >= OLED_RES_Y - enem.height:
                self.enemies.remove(enem)
                self.position[enem.X // 11] = enem.X
                self.health -= 1

            if self.is_player_got_hit(enem):
                self.health.pop()
                self.enemies.remove(enem)
                self.position[enem.X // 11] = enem.X

        self.oled.text(str(self.score), 0, 0)
        for heart in self.health:
            self.oled.blit(heart.fb, heart.X, heart.Y)

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
                if enem.is_enemy_got_hit(bul):
                    self.bullets.remove(bul)
                    self.enemies.remove(enem)
                    self.position[enem.X // 11] = enem.X
                    self.score += 2

    def fire(self):
        self.bullets.append(Bullet(self, self.oled))

    def is_player_got_hit(self, enemy):
        return (enemy.X <= self.X <= enemy.X + enemy.width or enemy.X <= self.X + self.width <= enemy.X + enemy.width) and enemy.Y + enemy.height >= self.Y

    def spawn_enemy(self):
        _pos = [a for a in self.position if a != -1]
        if _pos:  # if threashold reached
            X = random.choice(_pos)
            self.position[X // 11] = -1
            self.enemies.append(Enemy(self.oled, X))


class Bullet:
    def __init__(self, player: Player, oled):
        self.width = 1
        self.height = 3
        self.img = bytearray(
            b'\x80\x80\x80\x80\x80\x80')
        self.fb = framebuf.FrameBuffer(
            self.img, self.width, self.height, framebuf.MONO_HLSB)
        self.X = player.X + player.width // 2
        self.Y = player.Y - player.height // 2
