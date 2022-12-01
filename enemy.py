import framebuf


class Enemy:
    # Solving Overlapping Enemy Problem
    def __init__(self, oled, X) -> None:
        self.width = 11
        self.height = 8
        self.__img = bytearray(
            b' \x80\x1f\x00?\x80n\xc0\xff\xe0\xbf\xa0\xa0\xa0\x1b\x00')
        self.__fb = framebuf.FrameBuffer(
            self.__img, self.width, self.height, framebuf.MONO_HLSB)
        self.X = X
        self.Y = 0
        self.oled = oled

    def render_enemy(self):
        self.oled.blit(self.__fb, self.X, self.Y)

    def move(self):
        self.Y += 1

    def is_enemy_got_hit(self, bullet):
        return bullet.Y <= self.Y + self.height and self.X <= bullet.X <= self.X + self.width
