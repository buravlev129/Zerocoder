
import os
import animal
from jsondb import JsonDb


class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []
        path_name = os.path.dirname(__file__)
        self.db_file = os.path.join(path_name, "zoo_db.json")

    def add_animal(self, animal):
        self.animals.append(animal)
        print(f"Added {animal.name} to the zoo.")

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        print(f"Added {staff_member.name} to the staff.")


    def save(self):
        data = [obj.to_dict() for obj in self.animals]
        staff = [obj.to_dict() for obj in self.staff]
        data.extend(staff)

        db = JsonDb(filename=self.db_file)
        db.write_data(data)

    def load(self):
        self.animals.clear()
        self.staff.clear()
        
        print("Загрузка базы данных...")
        db = JsonDb(filename=self.db_file)
        data = db.load_data()
        for row in data:
            for class_name, attributes in row.items():
                if class_name == "Crow":
                    #self.animals.append(animal.Crow(**attributes))
                    self.animals.append(animal.Crow.from_dict(attributes))
                elif class_name == "Sparrow":
                    #self.animals.append(animal.Sparrow(**attributes))
                    self.animals.append(animal.Sparrow.from_dict(attributes))
                elif class_name == "Cat":
                    self.animals.append(animal.Cat(**attributes))
                elif class_name == "Dog":
                    self.animals.append(animal.Dog(**attributes))
                elif class_name == "Snake":
                    self.animals.append(animal.Snake(**attributes))
                elif class_name == "Lizard":
                    self.animals.append(animal.Lizard(**attributes))

                elif class_name == "ZooKeeper":
                    self.staff.append(ZooKeeper(**attributes))
                elif class_name == "Veterinarian":
                    self.staff.append(Veterinarian(**attributes))
                else:
                    print(f"Неизвестное существо: {class_name}")
                    continue

        count = len(data)
        print(f"Обработано {count} записей.")
        return count



class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} is feeding {animal.name}.")

    def __str__(self):
        return f"Работник зоопарка {self.name}"

    def to_dict(self):
        return {f"{self.__class__.__name__}": {"name": self.name}}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("name"))


class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} is healing {animal.name}.")

    def __str__(self):
        return f"Ветеринар {self.name}"

    def to_dict(self):
        return {f"{self.__class__.__name__}": {"name": self.name}}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("name"))




if __name__ == "__main__":

    zoo = Zoo()
    if zoo.load() == 0:
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

    zoo.save()

    print("\nСотрудники зоопарка")
    for person in zoo.staff:
        print(person)

    print("\nСписок животных")
    for a in zoo.animals:
        print(a)
