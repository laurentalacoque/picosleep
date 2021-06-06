""" A 'breathing-led' program to help fall asleep (c) Laurent Alacoque June 2021 """
#Breathing led program comparable to the "dowdow"
from pulseled import Led,LedPack
import time
from random import randrange
import math

# Parameters for the breathing experiment
BREATHING_FREQ = (11, 5) #11 breathing/mn at start downto 5 breathing/mn at end
DURATION = 10 # 10 mn for the whole experiment

# Parameters for onboard led
LED_PIN = 25
MAX_LIGHT = 255 #in range [1 255] (for single led)

# Parameters for a soldered RGB led
RGB_PINS  = (13,14,15) # solder an RGB led directly to the GPIO13 GND GPIO14 GPIO15
MAX_RGB_VALUE = 0.6 # ratio [0-1] : this sets the maximum light value for RGB led
MAX_RGB_LIGHT   = (255,210,160) # out of 255. This is set manually so that the led appears white when using ledpack.set_percent(100)

USE_RGB_LED = False

def hsv2rgb(h, s, v):
    """ This function is borrowed from
    https://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/ """
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def pulse_led(led,percents,duration_secs=1.0, ramp_secs=1.0):
    """ pulse a led from 0 to percents
        stays on during duration_secs and transition down to off
        with a transition of ramp_secs
    """
    #start at zero
    led.set_percent(0)
    # ramp up
    led.transition_to(percents, transition_duration=ramp_secs)
    # stay on
    time.sleep(duration_secs)
    # ramp down
    led.transition_to(0)

def breathing_period(seconds_so_far, breath_freq_start = BREATHING_FREQ[0], breath_freq_end = BREATHING_FREQ[1], duration = DURATION):
    """ Calculate the number of seconds for a full breathing cycle after seconds_so_far """
    #y(min) = a x(min) + b
    a=(breath_freq_end - breath_freq_start) / duration
    b=breath_freq_start
    
    breath_per_min = a * (seconds_so_far/60.0) + b
    seconds_per_breath = 60.0 / breath_per_min
    return seconds_per_breath



def breathing_light(led, duration_min=DURATION):
    """ Main program """
    t_start = time.time()
    seconds_so_far = time.time() - t_start
    while(seconds_so_far / 60.0 < duration_min):
        
        # get the breathing period at "seconds_so_far"
        seconds_per_breath =  breathing_period(seconds_so_far)
        print("seconds_per_breath = %f"%seconds_per_breath)
        
        # pulse half of this time and sleep half of it
        if type(led) == LedPack:
            # a rgb led : calculate a random hue
            hue = randrange(0,359)
            # convert this hue to percent for R, G and B
            percents = tuple(x/2.55 for x in hsv2rgb(hue,1.0,MAX_RGB_VALUE))
        else:
            # a simple led
            percents = 100
            
        pulse_led(led, percents, duration_secs=seconds_per_breath/2)
        time.sleep(seconds_per_breath/2)
        
        # update seconds_so_far value
        seconds_so_far = time.time() - t_start


if __name__ == "__main__":
    if not USE_RGB_LED:
        # use onboard led
        breathing_light(Led(pin_number=LED_PIN, max_pwm=MAX_LIGHT))
    else:
        # use soldered RGB led
        breathing_light(LedPack(pin_numbers=RGB_PINS, max_pwms=MAX_RGB_LIGHT))
    
