import os
import pygame
import random

from tank import Tank
from enemy import Saucer


pygame.init()

dimentions = (800, 650)

screen = pygame.display.set_mode(dimentions)
pygame.display.set_caption("Test game animations")

mypath = os.path.dirname(__file__)
imagepath = os.path.join(mypath, "images")

bg = pygame.image.load(os.path.join(imagepath, "landscape_t3.png"))
bg = pygame.transform.scale(bg, dimentions)

tank = Tank((110,110))

enemies = []


def generate_enemies():
    lst = []
    for _ in range(3):
        size = random.randint(35, 55)
        speed_x = random.randint(3, 9)
        speed_y = random.randint(3, 9)
        x = random.randint(10, 350)
        y = random.randint(10, 350)
        lst.append(Saucer((size,size), (speed_x, speed_y), (x, y)))
    return lst

clock = pygame.time.Clock()
working = True
while working:

    screen.blit(bg, (0,0))
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            working = False
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT:
                tank.change_cource()
            if ev.key == pygame.K_SPACE:
                tank.shoot()
            if ev.key == pygame.K_e:
                enemies.extend(generate_enemies())

    for e in enemies:
        e.run(screen)

    tank.run(screen)
    for b in tank.bullets:
        b.run(screen)
        if b.is_in_explosion or b.finished:
            continue
        
        b_rec = b.get_rect()
        
        for e in enemies:
            e_rec = e.get_rect()
            if b_rec.colliderect(e_rec):
                b.do_explode()
                enemies.remove(e)

        if b.finished:
            tank.bullets.remove(b)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
