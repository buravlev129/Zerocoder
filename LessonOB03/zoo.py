
import animal


class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Added {animal.name} to the zoo.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Added {staff_member.name} to the staff.")



class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")

    def __str__(self):
        return f"Работник зоопарка {self.name}"


class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}.")

    def __str__(self):
        return f"Ветеринар {self.name}"


if __name__ == "__main__":

    zoo = Zoo()
    zoo.add_staff(ZooKeeper("Михалыч"))
    zoo.add_staff(ZooKeeper("Палыч"))
    zoo.add_staff(Veterinarian("Марь Иванна"))

    assert hasattr(zoo.staff[0], "feed_animal")
    assert hasattr(zoo.staff[2], "heal_animal")

    zoo.add_animal(animal.Crow("Маша", 10, wing_span=.3))
    zoo.add_animal(animal.Sparrow("Шустрый", 20, wing_span=2))
    zoo.add_animal(animal.Dog("Шарик", 6, fur_color="brown"))
    zoo.add_animal(animal.Dog("Бобик", 5, fur_color="black"))
    zoo.add_animal(animal.Snake("Змея", 5))
    zoo.add_animal(animal.Lizard("Ящерица", 5))


    print("\nСотрудники зоопарка")
    for person in zoo.staff:
        print(person)

    print("\nСписок животных")
    for a in zoo.animals:
        print(a)
