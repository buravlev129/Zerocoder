import os
import pygame
import random

from explosion import Explosion


class Shell:
    """
    Снаряд
    """

    def __init__(self, size=None, speed=None, xy=None):
        mypath = os.path.dirname(__file__)
        self.images_path = os.path.join(mypath, "images")
        self.size = size

        self.speed_x = 8
        self.speed_y = 8
        if not speed is None:
            self.speed_x = speed[0]
            self.speed_y = speed[1]

        self.x = 0
        self.y = 0
        if not xy is None:
            self.x = xy[0]
            self.y = xy[1]
        
        self.init_image_lists()
        self.explosion = None
        self.is_in_explosion = False
        self.is_fired = False


    def init_image_lists(self):
        self.frame_count = 4
        self.frame_index = 0
        self.frame_delay = 2
        self.frame_delay_index = 0

        self.images = []
        for xx in range(self.frame_count):
            name = f"bullet_sp_{xx}.png"
            file = os.path.join(self.images_path, name)
            img = pygame.image.load(file).convert_alpha()
            if not self.size is None:
                img = pygame.transform.scale(img, self.size)
                self.images.append(img)

        self.image = self.images[0]


    def do_explode(self):
        self.explosion = Explosion((64,64), (self.x, self.y))
        self.is_in_explosion = True


    def run(self, screen, x=None, y=None):
        self.screen = screen

        if self.is_fired:
            return

        if self.is_in_explosion:
            self.explosion.run(screen)
            if self.explosion.finished:
                self.explosion = None
                self.is_fired = True
            return

        self.frame_delay_index += 1
        if self.frame_delay_index >= self.frame_delay:
            self.frame_delay_index = 0

        if self.frame_delay_index != 0:
            screen.blit(self.image, (self.x, self.y))
            return

        self.y += self.speed_y
        self.x += self.speed_x

        self.frame_index += 1
        if self.frame_index >= self.frame_count:
            self.frame_index = 0

        self.image = self.images[self.frame_index]
        screen.blit(self.image, (self.x, self.y))


    @property
    def out_of_boundaries(self):
        if self.x > self.screen.get_width() or self.x < 0 or self.y > self.screen.get_height() or self.y < 0:
            return True
        return False

    @property
    def finished(self):
        if self.out_of_boundaries or self.is_fired:
            return True
        return False

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))


