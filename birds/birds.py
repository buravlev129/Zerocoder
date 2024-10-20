import os
import pygame
import random


class Bird:
    """
    Птичка
    """

    DIRECTION_FORWARD = 0
    DIRECTION_BACKWARD = 1
    ECHELON_UP = 0
    ECHELON_DOWN = 1

    def __init__(self, images_path, width=None, height=None):
        img = pygame.image.load(os.path.join(images_path, "bird-red.png"))
        if not width is None and not height is None:
            img = pygame.transform.scale(img, (width, height))

        self.image_forward = img
        self.image_backward = pygame.transform.flip(img, flip_x=True, flip_y=False)
        self.image = img
        self.course = self.DIRECTION_FORWARD
        self.echelon = self.ECHELON_UP
        self.direction_counter = 0
        self.direction_counter_limit = 80

        self.width = img.get_width()
        self.height = img.get_height()
        self.x = 0
        self.y = 0
        self.speed_x = 5
        self.speed_y = 2
        self.screen = None


    def choose_direction(self):
        if self.direction_counter > self.direction_counter_limit:
            self.course = random.choice([self.DIRECTION_FORWARD, self.DIRECTION_BACKWARD])
            self.echelon = random.choice([self.ECHELON_UP, self.ECHELON_DOWN])
            self.direction_counter = random.randint(0, self.direction_counter_limit)

            self.speed_x = random.randint(2, 5)
            self.speed_y = random.randint(1, 3)

            if self.run_forward:
                self.image = self.image_forward
            else:
                self.image = self.image_backward
        else:
            self.direction_counter += 1


    @property
    def run_forward(self):
        return self.course == self.DIRECTION_FORWARD

    @property
    def run_upward(self):
        return self.echelon == self.ECHELON_UP

    def change_course(self):
        self.course = self.DIRECTION_FORWARD if self.course == self.DIRECTION_BACKWARD else self.DIRECTION_BACKWARD
        self.direction_counter = 0
        if self.run_forward:
            self.image = self.image_forward
        else:
            self.image = self.image_backward

    def change_echelon(self):
        self.echelon = self.ECHELON_UP if self.echelon == self.ECHELON_DOWN else self.ECHELON_DOWN
        self.direction_counter = 0


    def display(self, screen, x=None, y=None):
        self.screen = screen
        self.x = x if not x is None else random.randint(0, screen.get_width())
        self.y = y if not y is None else random.randint(0, screen.get_height())
        screen.blit(self.image, (self.x, self.y))


    def run(self, x=None, y=None):
        if not x is None and not y is None:
            self.x = x
            self.y = y
        else:
            self.choose_direction()
            delta_x = self.speed_x if self.run_forward else -self.speed_x
            delta_y = self.speed_y if self.run_upward else -self.speed_y

            self.x += delta_x
            if self.x + self.width > self.screen.get_width() or self.x < 0:
                self.change_course()
                
            self.y += delta_y
            if self.y + self.height > self.screen.get_height() or self.y < 0:
                self.change_echelon()

        self.screen.blit(self.image, (self.x, self.y))



class GameoverPanel:
    """
    Представляет панель с сообщением "Game Over"
    """

    def __init__(self):
        self.main_text_size = 160
        self.prompt_text_size = 36
        self.gameover_font = pygame.font.Font(None, self.main_text_size)
        self.gamerestart_font = pygame.font.Font(None, self.prompt_text_size)
        self.main_text = self.gameover_font.render(f'Game Over!', True, (255, 100, 0))
        self.prompt_text = self.gamerestart_font.render(f'Нажмите пробел, чтобы продолжить', True, (255, 0, 100))


    def show(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        main_rect = self.main_text.get_rect(center=(width // 2, height // 2 - self.main_text_size / 2))
        prompt_rect = self.prompt_text.get_rect(center=(width // 2, height // 2 + self.prompt_text_size /2))
        screen.blit(self.main_text, main_rect.topleft)
        screen.blit(self.prompt_text, prompt_rect.topleft)



class Game:

    def __init__(self, width, height, title):
        pygame.init()
        pygame.font.init()

        self.score_font = pygame.font.Font(None, 36)
        self.gameover_font = pygame.font.Font(None, 160)
        self.gamerestart_font = pygame.font.Font(None, 36)

        self.width = width
        self.height = height
        self.dimentions = (width, height)
        self.title = title
        self.mypath = os.path.dirname(__file__)
        self.imagepath = os.path.join(self.mypath, "images")
        
        self.screen = pygame.display.set_mode(self.dimentions)
        pygame.display.set_caption(title)

        form_image = "bird-red.jpg"
        icon = pygame.image.load(os.path.join(self.imagepath, form_image)).convert_alpha()
        pygame.display.set_icon(icon)

        self.bg = pygame.image.load(os.path.join(self.imagepath, "landscape.png"))
        self.bg = pygame.transform.scale(self.bg, self.dimentions)

        self.working = True
        self.game_over = False
        self.objects = []


    def quit(self):
        pygame.display.quit()
        pygame.quit()

    def add_object(self, obj, x=None, y=None):
        obj.display(self.screen, x, y)
        self.objects.append(obj)


    def main_loop(self):
        clock = pygame.time.Clock()
        nscore = 0
        gmover = GameoverPanel()

        while self.working:
            clock.tick(30)

            mouse_x = None
            mouse_y = None
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.working = False
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.working = False
                    elif ev.key == pygame.K_SPACE:
                        nscore = 0
                        self.game_over = False

            self.screen.blit(self.bg, (0, 0))

            nscore += 5
            if nscore >= 2500:
                self.game_over = True
                gmover.show(self.screen)
            else:
                score_text = self.score_font.render(f'Score: {nscore}', True, (255, 255, 255))
                self.screen.blit(score_text, (10, 10))

            if not self.game_over:
                for ob in self.objects:
                    ob.run(mouse_x, mouse_y)

            pygame.display.flip()
            #pygame.display.update()
        
        if not self.working:
            self.quit()





if __name__ == "__main__":
    
    game = Game(850, 700, "Funny birds")
    try:
        game.add_object(Bird(game.imagepath, 70, 45))
        game.add_object(Bird(game.imagepath, 55, 35))
        game.add_object(Bird(game.imagepath, 30, 35))

        game.add_object(Bird(game.imagepath, 30, 35))

        game.main_loop()
    except Exception as ex:
        print(str(ex))
    finally:
        game.quit()

