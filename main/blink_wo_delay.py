# blink_wo_delay - non-blocking blink using a timer
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()


def tick(timer):
    global led
    led.toggle()


tim.init(freq=1.5, mode=Timer.PERIODIC, callback=tick)
