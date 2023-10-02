# web_IO - webserver to control multiple IO pins
# pin_type can be 'led', 'button', 'digital'(input), 'analog'(input)
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import sys
from Pico_W import PicoW_pins


# class Pin contains the attributes for each Pin
# label - text for naming the Pin
# pin_type - 'led', 'button', 'digital'(input), 'analog'(input)
# Pico - Pico pin number (1-40)
# gpio - RP2040 GPIO number (see pins.py for xreference)
# level - on/off, analog value/0, high/low
# set_IO_pins will assign values based on initial index.html form
# control_IO_pins will update 'level' based on control_IO.html form
class IO_Pin(object):
    def __init__(self, label, pin_type, Pico, gpio, level):
        self.label = label
        self.pin_type = pin_type
        self.Pico = Pico
        self.gpio = gpio
        self.level = level

    def __repr__(self):
        return f'{self.__class__.__name__}\
        ("{self.label}",\
        "{self.pin_type}",\
        {self.Pico},\
        {self.gpio},\
        {self.level})'


IO_pin_0 = IO_Pin('Yellow', 'led', 4, PicoW_pins[4][0], 0)
IO_pin_1 = IO_Pin('Green', 'led', 20, PicoW_pins[20][0], 0)
IO_pin_2 = IO_Pin('Red', 'led', 21, PicoW_pins[21][0], 0)
IO_pin_3 = IO_Pin('Blue', 'led', 29, PicoW_pins[29][0], 0)
IO_pin_4 = IO_Pin('SW1', 'digital', 5, PicoW_pins[5][0], 0)
IO_pin_5 = IO_Pin('SW2', 'digital', 19, PicoW_pins[19][0], 0)
IO_pin_6 = IO_Pin('SW3', 'digital', 22, PicoW_pins[22][0], 0)
IO_pin_7 = IO_Pin('SW4', 'digital', 24, PicoW_pins[24][0], 0)
IO_pins = [IO_pin_0, IO_pin_1, IO_pin_2, IO_pin_3, IO_pin_4,
           IO_pin_5, IO_pin_6, IO_pin_7]


# function called from index.html to setup the labels and IO pins
# request "r" has two lists, 'label' and 'pin'
def set_IO_pins(r):
    global IO_pins
    print(f"{IO_pins[0].label}")
    print(f"{r.getlist('label')=}")
    print(f"{r.getlist('Pico')=}")
    print(f"{r.getlist('pin_type')=}")
    labels = r.getlist('label')
    Pico_pins = r.getlist('Pico')
    pin_types = r.getlist('pin_type')

    for i, label in enumerate(labels):
        IO_pins[i] = IO_Pin(label,
                            pin_types[i],
                            int(Pico_pins[i]),
                            PicoW_pins[int(Pico_pins[i])][0],
                            0)
        if pin_types[i] == 'led':
            Pin(IO_pins[i].gpio, Pin.OUT, value=0)
        elif pin_types[i] == 'digital':
            Pin(IO_pins[i].gpio, Pin.IN)


# function called from control_IO.html to turn leds on/off
# if entry with empty list, all leds will be turned off
# else entry with list containing assigned labels will be turned on
def control_led(r_labels):
    global IO_pins
    print(f"{r_labels=}")
    if len(r_labels) == 0:
        for IO_pin in IO_pins:
            if IO_pin.pin_type == 'led':
                Pin(IO_pin.gpio, Pin.OUT, value=0)
                IO_pin.level = 0
    else:
        for IO_pin in IO_pins:
            if IO_pin.pin_type == 'led' and IO_pin.label in r_labels:
                Pin(IO_pin.gpio, Pin.OUT, value=1)
                IO_pin.level = 1
            else:
                Pin(IO_pin.gpio, Pin.OUT, value=0)
                IO_pin.level = 0


def web_server():
    # Required for WLAN on Pico W, 'machine' indicates Pico-based micropython
    # Will not differeniate between Pico and Pico W!
    if hasattr(sys.implementation, '_machine'):
        from wlan import connect
        if not (connect()):
            print(f"wireless connection failed")
            sys.exit()

    app = Microdot()
    Response.default_content_type = 'text/html'
    Request.socket_read_timeout = None

    @ app.route('mvp.css')
    def mvp(request):
        return send_file('templates/mvp.css', max_age=31536000)

    @ app.post('/control_IO.html')
    def control(request):
        global IO_pins
        print(f"{request.form.get('submit')=}")
        print(f"1 {request.form.getlist('label')=}")
        # if len(labels list) > 0, its first time through
        # set labels and pin assignments
        if request.form.get('submit') == 'Setup':
            print(f"2 {request.form.getlist('label')=}")
            set_IO_pins(request.form)

        # else, just turn the leds on/off
        elif request.form.get('submit') == 'Lights':
            print(f"3 {request.form.getlist('label')=}")
            control_led(request.form.getlist('label'))
        return render_template('control_IO.html', IO_pins)

    @ app.get('/')
    def index(request):
        return render_template('index.html', IO_pins)

    @ app.get('computer.svg')
    def computer_svg(request):
        return send_file('./computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.get('favicon.ico')
    def favicon_ico(request):
        return send_file('./favicon.png', max_age=31536000)

    app.run(port=5001, debug=True)


if __name__ == '__main__':
    web_server()
