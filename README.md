# IOT Based Space Invaders :rocket:

The space shooter genre is a very attractive game for all ages. Thus we have decided to make a Space Invader Game using Rasberry Pi Pico . It will be a 2-d, first person, shooting game. It will be similar to the classics, but the controls will be different, as we are using a joystick to control the player. Space Invaders is one of the most famous early video games. The game is about defending the Earth from Space Invaders (aliens) by shooting them down before they can land. But in this game, player is able to shoot using a push button and control using a joystick.

Since the 1970s, people started to take interest in using their computers as an entertainment environment, thus, the multi billion game industry was starting to take shape. Having presented earlier the sum of money this industry produces, we decided to have a go and create a game of our own. The game is developed for full-time entertainment and enthusiasms. It teaches the Gamer to be alert at every situation he/she faces, because if the Gamer is not fully alert and notice the enemy may crush the player.

The market for computer games is moving towards complex, photo-realistic 3D games. However, such games have long startup times and high learning curves. They also require a lot of power and time. Solitaire, Snake or Angry Birds are examples for the success of simple and easy to use games. They have a high fun factor, no learning curve and short startup times. As the duration of these games is short, they can be played in nearly every situation. We  want to have a simple and easy Space Invaders game and offer it for students.

This is project to prove that we can also make a simple game using Rasberry Pi Pico which is dual-core Arm Cortex processor and 2 Mb Flash Memory.

## Things Required :shopping_cart:

* Raspberry Pi Pico
* Breadboard
* Jumper wires
* Electromagnetic Buzzer 
* Push Button Tactile Switch
* Joystick Module
* 0.96-inch I2C OLED display(ssd 1306) 

## Circuit Diagram :robot:

![img](assets/circuit.png)

## Implementation :truck:

![img](assets/prototype.jpg)

## How to Setup? :thinking:

After making all the necessary connections, save all below files into your Raspberry Pi Pico.

```
.
├── configs.py
├── enemy.py
├── main.py
├── player.py
├── sound.py
└── ssd1306.py
```

And just run main.py, to start the game. :smile:
