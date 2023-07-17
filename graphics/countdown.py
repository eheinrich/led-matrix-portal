import time
import math
import displayio
import terminalio

from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from graphics.graphic import Graphic


class CountdownGraphic(Graphic):
    tick_interval_seconds = 1

    target_year = 2023
    target_month = 9
    target_day = 1

    show_text = True

    target_time = time.struct_time(
        # format of time tuple: https://docs.circuitpython.org/en/latest/shared-bindings/time/index.html#time.struct_time
        (
            target_year,
            target_month,
            target_day,
            0,
            0,
            0,
            4,
            -1,
            -1,
        )
    )

    # Current frame
    frame = 0

    # Colors
    orange = 0xb03404
    purple = 0x9c02d4
    red = 0xb00000

    @classmethod
    def get_days_remaining(cls):
        seconds_remaining = time.mktime(cls.target_time) - time.mktime(time.localtime())
        days_remaining = math.ceil(seconds_remaining / 60 / 60 / 24)
        return days_remaining

    @classmethod
    def get_text(cls):
        days_remaining = cls.get_days_remaining()
        if days_remaining < 0:
            text = "It's here!"
        elif days_remaining == 0:
            text = "Today!"
        else:
            text = '{0} day{1}'.format(days_remaining, 's' if days_remaining > 1 else '')
        return text

    @classmethod
    def draw(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        text = cls.get_text()
        draw_group.append(
            label.Label(bitmap_font.load_font('/fonts/RobotoCondensed-Bold-16.bdf'), color=cls.orange, text=text)
        )
        draw_group[0].x = (matrix.display.width - draw_group[0].bounding_box[2] + 1) // 2
        draw_group[0].y = matrix.display.height // 2

    @classmethod
    def on_tick(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        if cls.frame == 0:
            draw_group[0].text = cls.get_text()
            draw_group[0].color = cls.orange
            draw_group[0].x = (matrix.display.width - draw_group[0].bounding_box[2] + 1) // 2
            cls.frame = 1

        elif cls.frame == 1:
            draw_group[0].text = cls.get_text()
            draw_group[0].color = cls.purple
            draw_group[0].x = (matrix.display.width - draw_group[0].bounding_box[2] + 1) // 2
            cls.frame = 2

        elif cls.frame == 2:
            draw_group[0].text = ''
            cls.frame = 3

        elif cls.frame == 3:
            draw_group[0].color = cls.red
            draw_group[0].text = 'STRANGE'
            draw_group[0].x = (matrix.display.width - draw_group[0].bounding_box[2] + 1) // 2
            cls.frame = 0
