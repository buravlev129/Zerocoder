from abc import ABC, abstractmethod



class Animal(ABC):
    """
    Абстрактный класс для животных
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def make_sound(self):
        pass

    def eat(self):
        print(f"{self.name} is eating.")


class Bird(Animal):
    """
    Подкласс Птицы
    """
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}, {self.age} лет, размах крыльев: {self.wing_span}"


class Crow(Bird):
    """
    Подкласс Ворона
    """
    def __init__(self, name, age, wing_span):
        super().__init__(name, age, wing_span)

    def make_sound(self):
        print(f"{self.__class__.__name__} каркает.")

class Sparrow(Bird):
    """
    Подкласс Воробей
    """
    def __init__(self, name, age, wing_span):
        super().__init__(name, age, wing_span)

    def make_sound(self):
        print(f"{self.__class__.__name__} чирикает.")



class Mammal(Animal):
    """
    Подкласс Млекопитающее
    """
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}, {self.age} лет, цвет шерсти: {self.fur_color}"


class Cat(Mammal):
    """
    Кошка
    """
    def __init__(self, name, age, fur_color):
        super().__init__(name, age, fur_color)
        
    def make_sound(self):
        print(f"{self.__class__.__name__} мяукает.")

class Dog(Mammal):
    """
    Собака
    """
    def __init__(self, name, age, fur_color):
        super().__init__(name, age, fur_color)
        
    def make_sound(self):
        print(f"{self.__class__.__name__} тяфкает.")



class Reptile(Animal):
    """
    Подкласс Рептилии
    """
    def __init__(self, name, age, has_legs):
        super().__init__(name, age)
        self.has_legs = has_legs

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}, {self.age} лет, имеет ноги: {self.has_legs}"


class Snake(Reptile):
    """
    Змея
    """
    def __init__(self, name, age):
        super().__init__(name, age, has_legs=False)
        
    def make_sound(self):
        print(f"{self.__class__.__name__} шипит.")

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}, {self.age} лет, не имеет ног"

class Lizard(Reptile):
    """
    Ящерица
    """
    def __init__(self, name, age):
        super().__init__(name, age, has_legs=True)
        
    def make_sound(self):
        print(f"{self.__class__.__name__} свистит.")

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}, {self.age} лет, имеет 4 ноги"



# Функция для демонстрации полиморфизма
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()


if __name__ == "__main__":

    animals = [
        Crow("Маша", 10, wing_span=.3) ,
        Sparrow("Шустрый", 20, wing_span=2) ,
        Cat("Мурка", 5, fur_color="black") ,
        Dog("Шарик", 6, fur_color="brown") ,
        Snake("Змея", 5) ,
        Lizard("Ящерица", 5)
    ]

    print("Список животных")
    for animal in animals:
        print(animal)

    print("\nКакие звуки они издают")
    animal_sound(animals)
