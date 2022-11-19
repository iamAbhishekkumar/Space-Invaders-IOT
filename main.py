from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf


def get_actor_img():
    width, height = 9, 10
    img = bytearray(
        b'\x08\x00\x1c\x00\x14\x00\x14\x00\x1c\x00>\x00\x7f\x00\xff\x80\xdd\x80\x08\x00')
    # MONO_HLSB
    return framebuf.FrameBuffer(img, width, height, framebuf.MONO_HLSB)


pix_res_x = 128  # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution

# start I2C on I2C1 (GPIO 26/27)
i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)  # oled controller

# frame buff types: GS2_HMSB, GS4_HMSB, GS8, MONO_HLSB, MONO_VLSB, MONO_HMSB, MVLSB, RGB565

actor = get_actor_img()
oled.fill(0)  # clear the OLED
oled.blit(actor, 53, 32)  # show the image at location (x=0,y=0)
oled.show()  # show the new text and image
