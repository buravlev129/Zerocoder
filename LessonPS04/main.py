from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_wikipedia():
    driver = webdriver.Firefox()

    try:
        while True:
            query = input("Введите запрос для поиска на Википедии (или 'exit' для выхода): ")
            if query.lower() == 'exit':
                break

            driver.get("https://ru.wikipedia.org/wiki/Служебная:Поиск")
            search_box = driver.find_element(By.NAME, "search")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            time.sleep(6)  # Подождать загрузку страницы
            while True:
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Выйти из программы")

                choice = input("Введите номер действия: ")
                if choice == '1':
                    # Листать параграфы
                    paragraphs = driver.find_elements(By.CSS_SELECTOR, 'p')
                    for i, paragraph in enumerate(paragraphs):
                        print(f"Paragraph {i+1}:\n{paragraph.text}\n")
                        if input("Нажмите Enter для продолжения или введите 'stop' для остановки: ").lower() == 'stop':
                            break

                elif choice == '2':
                    # Показать связанные страницы
                    links = driver.find_elements(By.CSS_SELECTOR, 'a')
                    related_links = [(link.text, link.get_attribute('href')) for link in links if link.text]

                    if not related_links:
                        print("Связанные страницы отсутствуют.")
                        continue
                    for i, (title, _) in enumerate(related_links):
                        print(f"{i+1}. {title}")

                    link_choice = input("Введите номер страницы, чтобы перейти на нее (или 'back' для возврата): ")
                    if link_choice.lower() == 'back':
                        continue

                    try:
                        link_index = int(link_choice) - 1
                        _, link_url = related_links[link_index]
                        driver.get(link_url)
                        time.sleep(2)  # Подождать загрузку страницы
                    except (ValueError, IndexError):
                        print("Некорректный выбор. Попробуйте снова.")

                elif choice == '3':
                    # Выйти из программы
                    print("Выход из программы.")
                    return

                else:
                    print("Некорректный выбор. Попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    search_wikipedia()




