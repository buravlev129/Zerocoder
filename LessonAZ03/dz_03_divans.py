import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


start_url = "https://divan.ru/category/divany-i-kresla"

driver = webdriver.Chrome()
driver.get(start_url)
time.sleep(5)

lightings = driver.find_elements(By.CSS_SELECTOR, 'div._Ud0k')
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

        print(name, price, currency, url)

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

    data.append([name, price, currency, url])

driver.quit()


target_file = "divans.csv"
path = os.path.dirname(__file__)
data_path = os.path.join(path, target_file)

if data:
    with open(data_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Price', 'Currency', 'Url'])
        writer.writerows(data)


