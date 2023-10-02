# pin_test.py - interactive app to test pins on a board
# uses Pico W pin number (1-40) as the input
import machine
import time

PicoW_pins = [[0, 'Not a pin'],     # 0 Index, not a valid pin
              [0, 'UART0 TX'],      # Pin 1
              [0, 'UART0 RX'],
              [0, 'GND'],
              [2, 'GP2'],
              [3, 'GP3'],
              [4, 'GP4'],
              [5, 'GP5'],
              [0, 'GND'],
              [6, 'GP6'],
              [7, 'GP7'],         # Pin 10
              [8, 'GP8'],
              [9, 'GP9'],
              [0, 'GND'],
              [10, 'GP10'],
              [11, 'GP11'],
              [12, 'GP12'],
              [13, 'GP13'],
              [0, 'GND'],
              [14, 'GP14'],
              [15, 'GP15'],         # Pin 20
              [16, 'GP16'],
              [17, 'GP17'],
              [0, 'GND'],
              [18, 'GP18'],
              [19, 'GP19'],
              [20, 'GP20'],
              [21, 'GP21'],
              [0, 'GND'],
              [22, 'GP22'],
              [0, 'RUN'],         # Pin 30
              [0, 'ADC0'],
              [0, 'ADC1'],
              [0, 'AGND'],
              [0, 'ADC2'],
              [0, 'ADC_REF'],
              [0, '3V3(OUT)'],
              [0, '3V3_EN'],
              [0, 'GND'],
              [0, 'VSYS'],
              [0, 'VBUS']         # Pin 40
              ]

minTest = 1
maxTest = 3

maxPins = 40


def print_header():
    print("Running Pico Pin Test:")
    print("""Tests: 0=> new pin 1=> High 2=> Low  3=> Blink once""")


def PinTest():
    startState = True
    testState = True
    print_header()

    while startState:
        pin = getPin()
        if pin >= 0:
            startState = False
            pinT = machine.Pin(pin, machine.Pin.OUT)

    while testState:
        test = getTest()
        if test >= 0:
            if test == 0:
                startState = True
                testState = False

            elif test == 1:  # 1 - set pin HIGH
                runTest_1(pinT)
                testState = True

            elif test == 2:  # 1 - set pin LOW
                runTest_2(pinT)
                testState = True

            elif test == 3:  # 1 - set pin to BLINK
                runTest_3(pinT)
                testState = True

            else:  # print error, not a valid test number
                print(test, "entered. Must be 0, 1, 2, or 3")
                testState = True


def getPin():
    pin = int(input("Enter pin number (1-40) to test: "))
    if (pin > maxPins):
        print("Error, pin requested", pin,
              " > number of board pins:", maxPins)
        pin = -1
    elif (pin < 0):
        print("Error, pin requested", pin, " < 0:")
        pin = -1
    else:
        if PicoW_pins[pin][0] == 0:
            print('Pin', pin, PicoW_pins[pin][1], "is not a GPIO pin")
            pin = -1
        else:
            print('Pin', pin, PicoW_pins[pin][1], ' enabled as Output')
            pin = PicoW_pins[pin][0]
    return(pin)


def getTest():
    test = int(input("Enter test to run: "))
    if test > maxTest:
        print("Error, test requested", test, "> tests allowed ")
        test = -1
    elif (test == 0):
        print("Restarting")
    elif test < minTest:
        print("Error, test requested", test, "< 0")
        test = -1
    return(test)


def blink(pin):
    pin.value(1)  # sets the digital pinN on
    time.sleep_ms(50)            # waits for a second
    pin.value(0)  # sets the digital pinN on
    time.sleep_ms(50)            # waits for a second


def runTest_1(pin):
    pin.value(1)
    print(pin, " is High")


def runTest_2(pin):
    pin.value(0)
    print(pin, " is LOW")


def runTest_3(pin):
    print(pin, " will blink once")
    blink(pin)


# delay required for serial connection to start
time.sleep_ms(1500)
while True:
    PinTest()
