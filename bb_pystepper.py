""" 
bb_pystepper is a Python module used to control a stepper motor via the 
BeagleBone
"""

from __future__ import division
import Adafruit_BBIO.GPIO as GPIO
import time
import math


def initialize_pins(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

def set_all_pins_low(pins):
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

def wavedrive(pins, pin_index):
    for i in range(len(pins)):
        if i == pin_index:
            GPIO.output(pins[i], GPIO.HIGH)
        else:
            GPIO.output(pins[i], GPIO.LOW)

def fullstep(pins, pin_index):
    """pin_index is the lead pin"""
    GPIO.output(pins[pin_index], GPIO.HIGH)
    GPIO.output(pins[(pin_index+3) % 4], GPIO.HIGH)
    GPIO.output(pins[(pin_index+1) % 4], GPIO.LOW)
    GPIO.output(pins[(pin_index+2) % 4], GPIO.LOW)

class Solenoid(object):
    def __init__(self, pin = "P8_17"):
        self.pins = [pin]
        initialize_pins(self.pins)
        set_all_pins_low(self.pins)

    def shoot(self):
        GPIO.output(self.pins[0], GPIO.HIGH)
        time.sleep(.00003)
        GPIO.output(self.pins[0], GPIO.LOW)



class Stepper(object):
    def __init__(self, rev_steps = 2048.0, pins = ["P8_13", "P8_14", "P8_15", "P8_16"]):
        in1 = pins[0]
        in2 = pins[1]
        in3 = pins[2]
        in4 = pins[3]

        self.pins = [in1, in2, in3, in4]

        initialize_pins(self.pins)
        set_all_pins_low(self.pins)

        self.angle = 0
        self.steps_per_rev = 2048.0

        # Initialize stepping mode
        self.drivemode = fullstep

    def rotate(self, degrees=360, rpm=15):
        step = 0

        # Calculate time between steps in seconds
        wait_time = 60.0/(self.steps_per_rev*rpm)

        # Convert degrees to steps
        steps = math.fabs(degrees*self.steps_per_rev/360.0)
        self.direction = 1

        if degrees < 0:
            self.pins.reverse()
            self.direction = -1

        while step < steps:
            for pin_index in range(len(self.pins)):
                self.drivemode(self.pins, pin_index)
                time.sleep(wait_time)
                step += 1
                self.angle = (self.angle + self.direction/self.steps_per_rev \
                *360.0) % 360.0

        if degrees < 0:
    		self.pins.reverse()

        set_all_pins_low(self.pins)

    def zero_angle(self):
        self.angle = 0

def main():
    stepper = Stepper()
    stepper.rotate()

if __name__ == "__main__":
    main()
