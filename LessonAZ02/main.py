import pandas as pd
import matplotlib.pyplot as plt
import random


names = [
    "Александр Смирнов", "Дмитрий Иванов", "Максим Кузнецов", "Анастасия Попова",
    "Екатерина Соловьёва", "Мария Васильева", "Иван Петров", "Светлана Михайлова",
    "Андрей Федоров", "Ольга Лебедева"
]

subjects = ['Математика', 'Физика', 'Химия', 'История', 'Литература']
data = {
    'Имя': [],
    'Математика': [],
    'Физика': [],
    'Химия': [],
    'История': [],
    'Литература': []
}

for name in random.sample(names, 10):
    data['Имя'].append(name)
    data['Математика'].append(random.randint(1, 5))
    data['Физика'].append(random.randint(1, 5))
    data['Химия'].append(random.randint(1, 5))
    data['История'].append(random.randint(1, 5))
    data['Литература'].append(random.randint(1, 5))

df = pd.DataFrame(data)

# 2. Вывод первых нескольких строк DataFrame
print("Первые несколько строк DataFrame:")
print(df.head())


# 3. Средняя оценка по каждому предмету
print("\nСредняя оценка по каждому предмету:")
mean_scores = df.select_dtypes(include='number').mean()
print(mean_scores)


# 4. Медианная оценка по каждому предмету
print("\nМедианная оценка по каждому предмету:")
median_scores = df.select_dtypes(include='number').median()
print(median_scores)


# 5. Q1 и Q3 для оценок по математике
Q1_math = df['Математика'].quantile(0.25)
Q3_math = df['Математика'].quantile(0.75)
print(f"\nQ1 для Математики: {Q1_math}")
print(f"Q3 для Математики: {Q3_math}")


# 6. Вычисление IQR
IQR_math = Q3_math - Q1_math
print(f"\nIQR для Математики: {IQR_math}")


# 7. Стандартное отклонение по каждому предмету
print("\nСтандартное отклонение по каждому предмету:")
std_scores = df.select_dtypes(include='number').median()
print(std_scores)


# Визуализация средних оценок
plt.figure(figsize=(10, 6))
mean_scores.plot(kind='bar', color='skyblue')
plt.title('Средняя оценка по каждому предмету')
plt.xlabel('Предмет')
plt.ylabel('Средняя оценка')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


