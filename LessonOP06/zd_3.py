import random

def select_students(students, num_to_select=5):
    """
    Выбирает случайным образом указанное количество уникальных имён из списка учащихся.
    
    :param students: список имён учащихся
    :param num_to_select: количество учащихся, которых нужно выбрать
    :return: список выбранных имён
    """
    if num_to_select > len(students):
        raise ValueError("Количество учащихся для выбора больше, чем количество доступных учащихся.")
    
    return random.sample(students, num_to_select)

def main():
    # Пример списка учащихся
    students = [
        "Алексей", "Мария", "Иван", "Ольга", "Дмитрий",
        "Екатерина", "Антон", "Светлана", "Павел", "Елена",
        "Максим", "Анастасия", "Сергей", "Ирина", "Владимир"
    ]
    
    try:
        selected_students = select_students(students, 5)
        print("Выбранные учащиеся:", selected_students)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
