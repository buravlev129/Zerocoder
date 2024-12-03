import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.divan.ru/category/svet"

driver.get(url)
time.sleep(3)

lightings = driver.find_elements(By.CSS_SELECTOR, 'div.WdR1o')
data = []

for light in lightings:
    try:
        root = light.find_element(By.CSS_SELECTOR, 'div.lsooF')

        name = root.find_element(By.CSS_SELECTOR, 'span').text

        prices = root.find_element(By.XPATH, 'div[@class="pY3d2"]/div/span[@class="ui-LD-ZU KIkOH" and @data-testid="price"]')
        price = prices.text.strip()
        price = price.replace(" ", "")
        currency = prices.find_element(By.CSS_SELECTOR, 'span').text.strip()

        if price:
            if currency and price.endswith(currency):
                price = price[0: price.find(currency)]
        else:
            price = "Не указана"

        url = light.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

        # print(name, price, currency, url)

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    data.append([name, price, currency, url])

driver.quit()


if data:
    with open("lightings.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название прибора', 'Цена', 'Валюта', 'Ссылка на страницу'])
        writer.writerows(data)




