# hello - simple test to show the time required to connect to serial monitor
import sys
import time


def Hello():
    i = 0
    while i < 100:
        print(f"{i*10}ms Hello, World!")
        time.sleep_ms(10)
        i += 1


if __name__ == '__main__':
    Hello()
    sys.exit()
