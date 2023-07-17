import gc
import time
import board
import displayio
from digitalio import DigitalInOut, Pull
from rtc import RTC

from adafruit_debouncer import Debouncer
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.network import Network

from graphics.happy_birthday import HappyBirthdayGraphic
from graphics.countdown import CountdownGraphic
from secrets import secrets

# --- Display setup ---
BITPLANES = 6  # Can set lower if RAM is tight
MATRIX = Matrix(bit_depth=BITPLANES)
GROUP = displayio.Group()

# --- Network setup ---
# Network credentials are pulled from `secrets.py`
NETWORK = Network(status_neopixel=board.NEOPIXEL, debug=False)
NETWORK.connect()

# --- Button setup ---
pin_down = DigitalInOut(board.BUTTON_DOWN)
pin_down.switch_to_input(pull=Pull.UP)
button_down = Debouncer(pin_down)
pin_up = DigitalInOut(board.BUTTON_UP)
pin_up.switch_to_input(pull=Pull.UP)
button_up = Debouncer(pin_up)


class RotatableGraphics:
    _graphics = [
        HappyBirthdayGraphic,
        CountdownGraphic
    ]
    _index = 0

    @classmethod
    def current(cls):
        return cls._graphics[cls._index]

    @classmethod
    def next(cls):
        if cls._index >= len(cls._graphics) - 1:
            cls._index = 0
        else:
            cls._index += 1

        return cls.current()

    @classmethod
    def prev(cls):
        if cls._index == 0:
            cls._index = len(cls._graphics) - 1
        else:
            cls._index -= 1

        return cls.current()


class SystemTime:
    update_every_seconds = 30 * 60  # 30 minutes
    last_update = time.monotonic() - update_every_seconds

    @classmethod
    def _update_system_time(cls, network: Network):
        """
        Update system clock date/time. Then local time is pulled from the World Time API, and is
        estimated using IP address. Reference: http://worldtimeapi.org/pages/examples
        """
        try:
            result = network.fetch('http://worldtimeapi.org/api/ip').json()
            # The 'datetime' field is in the format '2023-07-11T17:37:18.570876-07:00'. Replace all special
            # characters with spaces to make it easy to split and get the relevant bits from the resulting list
            local_datetime = result['datetime'].replace('-', ' ').replace('T', ' ').replace(':', ' ').split(' ')
            year = int(local_datetime[0])
            month = int(local_datetime[1])
            day = int(local_datetime[2])
            hour = int(local_datetime[3])
            minute = int(local_datetime[4])
            second = int(float(local_datetime[5]))
            now = time.struct_time((
                year,
                month,
                day,
                hour,
                minute,
                second,
                int(result['day_of_week']),
                int(result['day_of_year']),
                result['dst']
            ))
            RTC().datetime = now
        except Exception as e:
            print('Failed to update system time')
            print(e)

    @classmethod
    def refresh(cls, network: Network):
        current_time = time.monotonic()
        if current_time - cls.last_update > cls.update_every_seconds:
            print('Refreshing system time')
            cls._update_system_time(network)
            cls.last_update = current_time


SystemTime.refresh(NETWORK)
RotatableGraphics.current().setup(MATRIX, GROUP)

while True:
    # Collect garbage
    gc.collect()

    # Refresh system time
    SystemTime.refresh(NETWORK)

    # Check if buttons were clicked
    button_down.update()
    button_up.update()

    if button_up.fell:
        print("Clicked up")
        RotatableGraphics.prev().setup(MATRIX, GROUP)

    if button_down.fell:
        print("Clicked down")
        RotatableGraphics.next().setup(MATRIX, GROUP)

    # Update the graphic
    RotatableGraphics.current().tick(MATRIX, GROUP)
