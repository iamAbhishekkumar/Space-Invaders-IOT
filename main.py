from configs import *
from player import Player
from time import sleep


try:
    from ssd1306 import SSD1306_I2C
    from machine import Pin, I2C, ADC
    import utime
except ImportError:
    print("Something is wrong while importing libs")


def button1_pressed(pin):
    global button_presses, last_time
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - last_time) > 200:
        button_presses += 1
        last_time = new_time


def play(player, old_presses, move_enemy):
    global is_time_to_spawn, run, menu

    while run:
        xValue = X_AXIS.read_u16()
        yValue = Y_AXIS.read_u16()
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
            if menu:
                menu = False
                player = Player(OLED)
                play(player, 0, 0)

        move_enemy += 1
        is_time_to_spawn += 1
        if move_enemy > ENEMY_MOVEMENT_THRESHOLD:
            move_enemy = 0
            for enemy in player.enemies:
                enemy.move()

        OLED.fill(0)  # clear the OLED
        player.render_player()
        OLED.show()

        if is_time_to_spawn > ENEMY_SPAWN_THRESHOLD:
            is_time_to_spawn = 0
            player.spawn_enemy()
        player.handle_bullets()
        if player.health == 0:
            run = False
            menu = True
            blink_counter = 0
            while menu:
                OLED.fill(0)
                OLED.text("Game Over", 30, 15)
                OLED.text("To Play Again", 15, 35)
                blink_counter += 1
                if blink_counter > 30:
                    OLED.text("---Press Fire---", 0, 50)
                    blink_counter = 0
                    OLED.show()
                    sleep(1)
                OLED.show()
                if button_presses != old_presses:
                    old_presses = button_presses
                    menu = False
                    run = True
                    player = Player(OLED)
                    play(player, 0, 0)


# frame buff types: GS2_HMSB, GS4_HMSB, GS8, MONO_HLSB, MONO_VLSB, MONO_HMSB, MVLSB, RGB565

# Main.py
if __name__ == '__main__':

    last_time = 0  # the last time we pressed the button
    button_presses = 0
    is_time_to_spawn = 0

    # start I2C on I2C1 (GPIO 26/27)
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
    OLED = SSD1306_I2C(OLED_RES_X, OLED_RES_Y, i2c)  # oled controller
    X_AXIS = ADC(Pin(27))
    Y_AXIS = ADC(Pin(26))
    push_button = Pin(15, Pin.IN, Pin.PULL_UP)
    push_button.irq(handler=button1_pressed, trigger=Pin.IRQ_RISING)

    run = True
    menu = False

    player = Player(OLED)
    old_presses = 0
    move_enemy = 0

    play(player, old_presses, move_enemy)
