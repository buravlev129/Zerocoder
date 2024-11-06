import os
import pygame
import random


class Explosion:
    """
    Представляет взрыв
    """

    def __init__(self, size=None, xy=None):
        mypath = os.path.dirname(__file__)
        self.images_path = os.path.join(mypath, "images")
        self.size = size

        self.x = 0
        self.y = 0
        if not xy is None:
            self.x = xy[0]
            self.y = xy[1]
        
        self.init_image_lists()


    def init_image_lists(self):
        self.frame_count = 11
        self.frame_index = 0
        self.frame_delay = 2
        self.frame_delay_index = 0

        self.images = []
        for xx in range(self.frame_count):
            name = f"vzryv_{xx:02}.png"
            file = os.path.join(self.images_path, name)
            img = pygame.image.load(file).convert_alpha()
            if not self.size is None:
                img = pygame.transform.scale(img, self.size)
                self.images.append(img)

        self.image = self.images[0]


    def run(self, screen, x=None, y=None):
        self.screen = screen
        if self.finished:
            return
        
        self.frame_delay_index += 1
        if self.frame_delay_index >= self.frame_delay:
            self.frame_delay_index = 0

        width, height = self.image.get_size()
        draw_x = self.x - width // 2
        draw_y = self.y - height // 2        

        if self.frame_delay_index != 0:
            screen.blit(self.image, (draw_x, draw_y))
            return

        if self.frame_index >= self.frame_count:
            self.frame_index = 0

        self.image = self.images[self.frame_index]
        self.frame_index += 1

        screen.blit(self.image, (draw_x, draw_y))


    @property
    def finished(self):
        return self.frame_index >= self.frame_count

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

