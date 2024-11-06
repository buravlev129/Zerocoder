import pygame
import random


class Saucer:
    """
    Летающая тарелка
    """

    def __init__(self, size=None, speed=None, xy=None):
 
        self.size = (50,50) if size is None else size

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

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        center = self.size[0] / 2.0
        radius = center * 0.9
        img = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        pygame.draw.circle(img, color, (center,center), radius)      
        self.image = img


    def run(self, screen, x=None, y=None):
        self.screen = screen
        if self.finished:
            return
        
        img_width = self.image.get_width()
        img_height = self.image.get_height()
        scr_width = screen.get_width()
        scr_height = screen.get_height()
        if self.x > scr_width - img_width or self.x < 0:
            self.speed_x = -self.speed_x
        if self.y > scr_height - img_height or self.y < 0:
            self.speed_y = -self.speed_y

        self.x += self.speed_x
        self.y += self.speed_y

        screen.blit(self.image, (self.x, self.y))


    @property
    def finished(self):
        return False

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))


