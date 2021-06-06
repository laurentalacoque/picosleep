# picosleep - Raspberry pico sleep aid device

## In brief
PicoSleep is a program that helps you fall asleep.

It runs on the [raspberry pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) platform and pulses the onboard led (or a soldered RGB led) with a slowly decreasing frequency.

Synchronize your breathing with the led pulses to decrease your heart and breathing rates and help yourself fall asleep.

[![picoSleep with an RGB led and a star origami in action](https://img.youtube.com/vi/jH4l7bzbc8k/0.jpg)](https://youtu.be/jH4l7bzbc8k)

## Do it yourself

### 1. Get your raspberry pico and set it up
**raspberry pico** are inexpensive computing platforms that interact with the world.

See the [official raspberry site](https://www.raspberrypi.org/products/raspberry-pi-pico/) to get one and set it up

### 2. Upload the source to your pico
There are several ways to do this, please refer to the official doc to understand how.

Keep in mind that you should upload two files on your raspberry:
- `pulseled.py` (a helper module to deal with leds and pulsing)
- `main.py` (the main program)

Once this is done, you can disconnect the pico and plug it again to a power source : the onboard green led should now be pulsing

[![picoSleep pulsing onboard led](https://img.youtube.com/vi/Mms6qdON9Jg/0.jpg)](https://youtu.be/Mms6qdON9Jg)

**Done : you can enjoy your sleep aid platform :)**

### 3. Not satisfied ? Improve the PicoSleep with an RGB led

#### Get your RGB led

RGB Leds are inexpensive devices that can produce a colored light.

Try to find a LED reseller somewhere and keep in mind that you want a 4 pins led.

Here's what they look like:

![RGB leds](https://images-na.ssl-images-amazon.com/images/I/51HtFIKx3jL._AC_.jpg)

The most important thing to note is that **the longest pin is the ground** and it should be soldered to a pico `GND` pin.

#### Insert your RGB led on the pico

- At first, no need to solder anything, just insert your freshly bought RGB led in the pico holes labeled `GP13` - `GND` - `GP14` - `GP15`. The longest pin should go into the `GND` hole.

- Make a slight change to `main.py` program by changing
  - `USE_RGB_LED = False`
  to
  - `USE_RGB_LED = True`

- Disconnect and reconnect your pico : you should see the led change color at each breathing cycle

Satisfied ? Just solder the led to your pico board and voilà :)

#### Origami led cover
Although your PicoSleep is finished now, you may want to cover the led with a cover to contain and smoothen the led's light

I made an origami star led cover, see this tutorial for how to do it: 

[![Origami led cover](https://img.youtube.com/vi/RntZNBrfrQo/0.jpg)](https://youtu.be/RntZNBrfrQo)

Note: I used a 1.5 cm x 30 cm band of plain paper for the cover.

## 4. Tune things up

Most important parameters are at the top of `main.py` file, here's a description for them:

### Breathing parameters

- `BREATHING_FREQ = (11, 5)` controls the breathing rate at (start, end) of the experience. They're set to 11 breathing per minute at start down to 5 breathing per minute at end
- `DURATION = 10` controls the duration of the experience (10 mn by default)

### Monochromous led parameters

- `LED_PIN = 25` the pin that controls the led (by default, this is the onboard led but you can solder any led between `GND` and `GPxx` and put the `xx` number here)
- `MAX_LIGHT = 255` the led maximum power in the range [1 - 255]

### RGB led parameters

- `RGB_PINS  = (13,14,15)` the GPIOs where you soledered your respectively Red, Green and Blue pins
- `MAX_RGB_VALUE = 0.6` the maximum light power for the RGB led in the range [0 - 1.0]
- `MAX_RGB_LIGHT   = (255,210,160)` this is a preset of the relative power of each led and depends on the led maker and model and acts as a color balance. If you feel that the colors lack of Red, Green or Blue, try to change the channel intensity here.

- `USE_RGB_LED = False` whether to use the soldered RGB led (set this to `True`) or the onboard monochromous led (leave this to `False`)





