import random
from abc import ABC, abstractmethod



class Weapon(ABC):
    def __init__(self):
        self.name = ""
        self.power = 0

    @abstractmethod
    def attack(self, enemy):
        pass


class Sword(Weapon):
    def __init__(self):
        self.name = "Меч"
        self.power = 15

    def attack(self, enemy):
        print("Атакует мечом")
        damage = int(self.power * random.choice([1.0, 0.5, 0.99, 0.3, 0.8, 1.5]))
        enemy.reduce_vitality(damage)


class Bow(Weapon):
    def __init__(self):
        self.name = "Посох"
        self.power = 3

    def attack(self, enemy):
        print("Атакует посохом")
        damage = int(self.power * random.choice([1.0, 0.3, 0.99, 0.3, 0.3, 1.5]))
        enemy.reduce_vitality(damage)


class Bazuka(Weapon):
    def __init__(self):
        self.name = "Базука"
        self.power = 55

    def attack(self, enemy):
        print("Атакует из базуки")
        damage = int(self.power * random.choice([1.0, 0.5, 0.99, 0.5, 0.8, 1.0]))
        enemy.reduce_vitality(damage)


class Fighter:
    def __init__(self):
        self.weapon = None

    def select_weapon(self, weapon):
        print(f"Боец: вибирает {weapon.name}")
        self.weapon = weapon

    def fight(self, enemy):
        if self.weapon:
            print(f"Боец:")
            self.weapon.attack(enemy)
        else:
            print("Пока нечем атаковать")


class Monster:
    def __init__(self):
        self.name = "Змей"
        self.vitality = 100

    def reduce_vitality(self, damage):
        print(f"{self.name}:")
        if damage < 2:
            print("Ой, не смеши")
        else:
            print("Атакован ", ">" * damage)

        self.vitality -= damage
        if self.vitality < 0:
            self.vitality = 0

        print(f"остаток силы: {self.vitality} {self.state}")


    def __str__(self):
        return f"{self.name}, сила: {self.vitality} {self.state}"

    @property
    def state(self):
        return "Живой" if self.vitality > 0 else "Убит"



if __name__ == "__main__":

    boy = Fighter()
    zmei = Monster()
    boy.fight(zmei)

    weapons = [Bow(), Sword(), Bazuka(), Bow(), Sword(), Bazuka(), Bow()]
    while True:
        choice = random.choice(weapons)

        boy.select_weapon(choice)
        boy.fight(zmei)
        if zmei.state != "Живой":
            break

    print("---")
