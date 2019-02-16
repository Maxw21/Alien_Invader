from pygame.sprite import Group

from barrier_pixel import BarrierPixel


class Barrier:
    """A class to hold the pieces of a barrier."""
    def __init__(self, screen, sprite_sheet, column):
        self.screen = screen
        self.sprite_sheet = sprite_sheet
        self.column = column
        self.barrier = Group()

    def create_barrier(self):
        """Creates the pixels that make up a single barrier"""
        x = 184
        y = 84
        for i in range(0, 60, 5):
            for j in range(0, 40, 4):
                barrier_pixel = BarrierPixel(screen=self.screen, sprite_sheet=self.sprite_sheet,
                                             x=(x + i), y=(y + j), column=self.column)
                self.barrier.add(barrier_pixel)

    def draw_barrier(self):
        """Draw the barrier on the screen."""
        for barrier_pixel in self.barrier:
            barrier_pixel.blitme()
