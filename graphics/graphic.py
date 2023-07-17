import time
import displayio
import terminalio

from adafruit_matrixportal.matrix import Matrix


class Graphic:
    # Override `update_interval_seconds` to set custom tick interval time
    tick_interval_seconds = 5
    _last_tick_seconds = time.monotonic()

    @classmethod
    def draw(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        """Override this method with the to draw something else."""
        draw_group.append(label.Label(terminalio.FONT, color=0xFF0000, text='Hello, world!'))
        draw_group[0].x = (matrix.display.width - draw_group[0].bounding_box[2] + 1) // 2
        draw_group[0].y = matrix.display.height // 2 - 1


    @classmethod
    def setup(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        """Calling this method will re-draw the graphic on the display."""
        print('Setting up graphic')
        while len(draw_group) > 0:
            del draw_group[0]
        cls.draw(matrix, draw_group)
        matrix.display.refresh()
        matrix.display.show(draw_group)

    @classmethod
    def on_tick(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        """Override this method to set the update behavior on tick"""
        pass

    @classmethod
    def tick(cls, matrix: Matrix, draw_group: displayio.Group, *args, **kwargs):
        current_time = time.monotonic()
        if current_time - cls._last_tick_seconds > cls.tick_interval_seconds:
            cls.on_tick(matrix, draw_group, *args, **kwargs)
            cls._last_tick_seconds = current_time
