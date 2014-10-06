################################################################################
#
# Copyright 2014, Jack Pien
# All rights reserved.
# http://www.jackpien.com
#
# Author: Jack Pien <jack.pien@af386.com>
#
# See license in LICENSE.txt file.
#
# This sample script turns a servo via PWM via pin 9
# depending on a voltage reading coming in on pin A0. This script uses
# the wiring-x86 library provided for by Emutex

import sys
import time
from wiringx86 import GPIOGalileo as GPIO

def main(argv):
    gpio = GPIO(debug=True)
    pin = 13
    state = gpio.HIGH
    servo_pin = 9
    gpio.pinMode(pin, gpio.OUTPUT)
    gpio.pinMode(servo_pin, gpio.PWM)
    

    # PWM period for G2 is same for all pins so second call is redundant
    pwm_period = 3000000
    gpio.setPWMPeriod(servo_pin, pwm_period)

    # Turn on LED
    gpio.digitalWrite(pin, gpio.HIGH)

    # Read analog input from pin 14
    adc_l = 14 # A0

    # Set pin 14 to be used as an analog input GPIO pin.
    gpio.pinMode(adc_l, gpio.ANALOG_INPUT)

    # With a 100 Ohm resistor and 3.3K resistor and 10k Pot the min max vals 
    # read from the ADC are around
    min_val = 204
    max_val = 994
    val_range = float(max_val - min_val)

    # Servo min and max pulse in ms
    min_pulse = 500000
    max_pulse = 2500000
    pulse_range = float(max_pulse-min_pulse)
    

    print 'Analog reading from pin %d now...' % adc_l
    try:
        old_pulse_length = 0

        while(True):
            value_l = gpio.analogRead(adc_l)
            
            print value_l
            print ""

            norm_val = float(value_l - min_val) / val_range
            norm_val = min( max(0.0, norm_val), 1.0 )

            print norm_val

            # What is duty cycle?
            pulse_length = (norm_val * pulse_range) + min_pulse
            pulse_pct = float(abs(pulse_length - old_pulse_length)) / \
                        float(pulse_length) 

            # Only write new duty cycle if there is significant change from 
            # previous value 
            if pulse_pct > 0.02:
                gpio.analogWrite(servo_pin, \
                                 int(float(pulse_length)/pwm_period * 255.0))
            else:
                pass
                
            old_pulse_length = pulse_length
            

            time.sleep(0.2)

    except KeyboardInterrupt:
        gpio.analogWrite(servo_pin, 0)

        # Leave the led turned off.
        gpio.digitalWrite(pin, gpio.LOW)


    print '\nCleaning up...'
    gpio.cleanup()


if __name__ == "__main__":
    main(sys.argv)
