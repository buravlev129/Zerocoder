
def add(a, b):
    """Функция для сложения двух чисел."""
    return a + b

def subtract(a, b):
    """Функция для вычитания одного числа из другого."""
    return a - b

def multiply(a, b):
    """Функция для умножения двух чисел."""
    return a * b

def divide(a, b):
    """Функция для деления одного числа на другое."""
    if b == 0:
        raise ValueError("Деление на ноль невозможно!")
    return a / b
