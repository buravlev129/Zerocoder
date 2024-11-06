

class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 20


    def attack(self, other):
        print(f"\n{self.name} атакует")
        other.health -= self.attack_power

    @property
    def is_alive(self):
        return self.health > 0

    def __str__(self):
        state = f"Здоровье: {self.health}" if self.health > 0 else "Убит"
        return f"{self.name} {state}"
    