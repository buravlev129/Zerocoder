
def main():
    # Запрос ввода от пользователя
    user_input = input("Введите текст, который хотите сохранить в файл: ")
    
    # Открытие файла в режиме записи
    with open("user_data.txt", "w", encoding="utf-8") as file:
        # Запись текста в файл
        file.write(user_input)
    
    print("Текст успешно записан в файл user_data.txt.")

if __name__ == "__main__":
    main()
