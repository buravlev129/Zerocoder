import os
import pandas as pd
import matplotlib.pyplot as plt


target_file = "divans.csv"
path = os.path.dirname(__file__)
data_path = os.path.join(path, target_file)

df = pd.read_csv(data_path)

# обработать данные: найти среднюю цену и вывести ее, а также сделать гистограмму цен на диваны​

average_price = df['Price'].mean()
print(f'Средняя цена на диваны: {average_price} ₽')

plt.hist(df['Price'], bins=20, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Количество')
plt.show()

