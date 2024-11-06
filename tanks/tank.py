import os
import pygame
import random

from ammo import Shell


class Tank:
    """
    Танк
    """

    DIRECTION_FORWARD = 0
    DIRECTION_BACKWARD = 1
    HEIGHT_UP = 0
    HEIGHT_DOWN = 1

    def __init__(self, size=None, echelon=0):
        mypath = os.path.dirname(__file__)
        self.images_path = os.path.join(mypath, "images")

        self.size = size
        self.speed_x = 5
        self.speed_y = 2
        self.course = self.DIRECTION_FORWARD
        self.height_direction = self.HEIGHT_UP
        self.random_cource_counter = 0
        self.echelon = echelon
        self.x = 0
        self.y = 0
        self.bullets = []

        self.init_image_lists()


    def init_image_lists(self):
        self.frame_count = 10
        self.frame_index = 0
        self.frame_delay = 3
        self.frame_delay_index = 0

        self.img_right = []
        self.img_left = []
        for xx in range(self.frame_count):
            name = f"tank_{xx:02}.png"
            file = os.path.join(self.images_path, name)
            img = pygame.image.load(file).convert_alpha()
            if not self.size is None:
                img = pygame.transform.scale(img, self.size)
                self.img_right.append(img)
                img = pygame.transform.flip(img, flip_x=True, flip_y=False)
                self.img_left.append(img)

        self.image = self.img_right[0]

    def build_body_image(self):
        surf = pygame.surface.Surface(self.size, pygame.SRCALPHA, 32)
        for part in self.look:
            name = self.look[part]
            file = os.path.join(self.images_path, name)
            img = pygame.image.load(file).convert_alpha()
            if not self.size is None:
                img = pygame.transform.scale(img, self.size)
            surf.blit(img, (0,0))
        return surf

    @property
    def run_forward(self):
        return self.course == self.DIRECTION_FORWARD

    @property
    def run_upward(self):
        return self.height_direction == self.HEIGHT_UP

    def change_height(self):
        self.height_direction = self.HEIGHT_UP if self.height_direction == self.HEIGHT_DOWN else self.HEIGHT_DOWN

    def change_cource(self):
        self.course = self.DIRECTION_FORWARD if self.course == self.DIRECTION_BACKWARD else self.DIRECTION_BACKWARD

    def random_change_cource(self):
        self.random_cource_counter += 1
        if self.random_cource_counter > 40:
            self.random_cource_counter = 0
            if random.random() > 0.8:
                self.change_cource()

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    def run(self, screen, x=None, y=None):
        self.screen = screen

        if self.echelon == 0:
            self.echelon = int(screen.get_height() * 0.7)
            self.y = self.echelon

        self.frame_delay_index += 1
        if self.frame_delay_index >= self.frame_delay:
            self.frame_delay_index = 0

        if self.frame_delay_index != 0:
            screen.blit(self.image, (self.x, self.y))
            return
        
        self.frame_index += 1
        if self.frame_index >= self.frame_count:
            self.frame_index = 0

        self.random_change_cource()

        if self.run_forward:
            self.image = self.img_right[self.frame_index]
        else:
            self.image = self.img_left[self.frame_index]

        delta_y = self.speed_y if self.run_upward else -self.speed_y
        self.y += delta_y
        if self.y > self.echelon * 1.05 or  self.y < self.echelon * 0.95:
            self.change_height()

        delta_x = self.speed_x if self.run_forward else -self.speed_x
        self.x += delta_x

        img_width = self.image.get_width()
        scr_width = screen.get_width()
        if self.run_forward:
            if self.x > scr_width:
                self.x = -img_width
        else:
            if self.x < -img_width:
                self.x = scr_width

        screen.blit(self.image, (self.x, self.y))

    def random_speed(self):
        speed = random.choice((8,9,10,11,12))
        if self.run_forward:
            dir_x = speed
            dir_y = -speed
        else:
            dir_x = -speed
            dir_y = -speed
        return (dir_x, dir_y)

    def shoot(self):
        pix_y = 50
        pix_x = 20
        if self.run_forward:
            x = self.x + self.image.get_width() - pix_x
            y = self.y + pix_y
        else:
            x = self.x + pix_x
            y = self.y + pix_y

        self.bullets.append(Shell((20, 20), self.random_speed(), (x, y-2)))
        self.bullets.append(Shell((18, 18), self.random_speed(), (x, y+2)))
        self.bullets.append(Shell((24, 24), self.random_speed(), (x+3, y-5)))


