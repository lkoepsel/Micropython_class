# echo_hex - print the hex equivilient of key pressed
import sys
import time
import uselect


spoll = uselect.poll()
spoll.register(sys.stdin, uselect.POLLIN)


def read_1char():
    return(sys.stdin.read(1) if spoll.poll(0) else None)


def show_key():
    key = read_1char()
    while key is None:
        key = read_1char()
    print(f"key: {key} dec: {ord(key)} hex: {hex(ord(key))}")
    return


if __name__ == '__main__':
    time.sleep(1)
    i = 0
    while i < 5:
        print(f"Press a key: ", end='')
        show_key()
        i += 1
    sys.exit()
