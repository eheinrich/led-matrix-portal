import displayio

from adafruit_matrixportal.matrix import Matrix
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.scrolling_label import ScrollingLabel

from graphics.graphic import Graphic


class HappyBirthdayGraphic(Graphic):
    tick_interval_seconds = 0.1

    scrolling_label = ScrollingLabel(
        bitmap_font.load_font('/fonts/helvB12.bdf'),
        text='Happy Birthday!!!',
        color=0x360236,
        max_characters=10,
        animate_time=0.3
    )

    @classmethod
    def draw(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        draw_group.append(cls.scrolling_label)
        cls.scrolling_label.x = 2
        cls.scrolling_label.y = matrix.display.height // 2 - 1

    @classmethod
    def on_tick(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        cls.scrolling_label.update()
