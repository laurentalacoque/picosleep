""" A module that use PWM to control the light of leds, ledpacks and add transitions 
    Author: Laurent Alacoque June 2021 """

from machine import Pin, PWM
import time

# Single led control
class Led:
    """ Single led control and transitionning """
    def __init__(self,pin_number=25,max_pwm=255, frequency = 1000):
        if max_pwm <= 0 or max_pwm > 255:
            raise ValueError("Bad value for max_pwm, should be [1 255]")
        self.max_pwm = max_pwm
        self.pin_number = pin_number
        # construct PWM object
        self.ledpwm  = PWM(Pin(self.pin_number))
        self.frequency = frequency
        self.ledpwm.freq(self.frequency)
        # start at off state
        self.percent = 0
        self.ledpwm.duty_u16(self.percent)
        self.steps_remaining = 0
        self.target = 0
    
    def set_percent(self,percent):
        """ Immediately set intensity to percent """
        if percent > 100.0:
            percent = 100.0
        if percent < 0.0:
            percent = 0.0
        self.percent = percent
        value = int(percent * self.max_pwm /100.0)
        self.ledpwm.duty_u16(value*value)
        
        
    def set_transition_to(self, percent, steps=100):
        """ Program a transition to `percent` in `steps` steps"""
        self.target = percent
        self.increment = (self.target - self.percent)/(1.0*steps)
        self.steps_remaining = steps
        
    def end_transition(self):
        """ Immediately end transition """
        self.set_percent(self.target)
        self.increment=0
        self.steps_remaining = 0
    
    def transition_step(self):
        """perform one nonblocking step of transition to target, return True when reached"""
        newvalue = self.percent + self.increment
        self.set_percent(newvalue)
        self.steps_remaining -= 1
        if self.steps_remaining <= 0:
            self.end_transition()
            return True
        else:
            return None
        
    def transition_to(self,target, transition_duration = 1.0):
        """ perform the full transition to the target. This is blocking """
        self.set_transition_to(target)
        sleep_time = (transition_duration / self.steps_remaining)
        while(not self.transition_step()):
            time.sleep(sleep_time)
        
class LedPack:
    """ Single led control and transitionning """
    def __init__(self,pin_numbers=(25,),max_pwms=(255,), frequency = 1000):
        self.leds = list()
        for pin, pwm in zip(pin_numbers,max_pwms):
            self.leds.append(Led(pin,pwm,frequency))

    def set_percent(self,percents):
        """ Immediately set intensity to percents 
            percents is either a number in the range [0 - 100] 
            or a tuple of numbers in the same range whose dimension
            equals the number of leds in this pack
        """
        if type(percents) == int or type(percents) == float:
            for led in self.leds:
                led.set_percent(percents)
        else:
            for led, perc in zip(self.leds, percents):
                led.set_percent(perc)
        
    def set_transition_to(self, percents, steps=100):
        """ Program a transition to `percents` in `steps` steps
            percents is either a number in the range [0 - 100] 
            or a tuple of numbers in the same range whose dimension
            equals the number of leds in this pack
        """
        if type(percents) == int or type(percents) == float:
            for led in self.leds:
                led.set_transition_to(percents,steps=steps)
        else:
            for led, perc in zip(self.leds, percents):
                led.set_transition_to(perc,steps=steps)
    
    def end_transition(self):
        """ Immediately end transition """
        for led in self.leds:
            self.end_transition()

    def transition_step(self):
        """perform one nonblocking step of transition to target, return True when reached"""
        for led in self.leds:
            led.transition_step()
        if self.leds[0].steps_remaining <= 0:
            return True
        return None

    def transition_to(self, targets, transition_duration = 1.0, steps=100):
        """ Starts a blocking transition to `targets`
            targets is either a number in the range [0 - 100] 
            or a tuple of numbers in the same range whose dimension
            equals the number of leds in this pack
        """
        if type(targets) == int or type(targets) == float:
            for led in self.leds:
                led.set_transition_to(targets,steps=steps)
        else:
            for led,target in zip(self.leds, targets):
                led.set_transition_to(target,steps=steps)
        sleep_time = ((transition_duration*1.0) / steps)
        for i in range(steps):
            for led in self.leds:
                led.transition_step()
            time.sleep(sleep_time)

if __name__ == "__main__":
    led = LedPack(pin_numbers=(13,14,15),max_pwms=(255,255,255))
