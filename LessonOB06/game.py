
import random
from hero import Hero


class Game:
    def __init__(self):
        self.hero = Hero("Илья Муромец")
        self.opponent = Hero("Змей")

    def start(self):

        print("Битва героев")
        print("-----------------")
        print(f"{self.hero}")
        print(f"{self.opponent}")
        print("---")

        while True:

            hero_turn = random.choice((False, True, True))
            if hero_turn:
                if self.hero.is_alive:
                    self.hero.attack(self.opponent)
                    print(f"{self.opponent}")
            else:
                if self.opponent.is_alive:
                    self.opponent.attack(self.hero)
                    print(f"{self.hero}")

            if not (self.hero.is_alive and self.opponent.is_alive):
                break






if __name__ == "__main__":

    game = Game()
    game.start()

    print("---")
