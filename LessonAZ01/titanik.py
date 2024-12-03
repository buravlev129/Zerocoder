import os
import pandas as pd

path = os.path.dirname(__file__)
path = os.path.join(path, "Titanik")
data_path = os.path.join(path, "titanic.csv")

df = pd.read_csv(data_path)

print("Первые 5 строк данных:")
print(df.head())

print("\nИнформация о данных:")
print(df.info())

print("\nСтатистическое описание:")
print(df.describe())


# print(df.columns)

# print(df[["Name", "Sex", "Age"]])

# print(df.loc[120, "Name"])

filtered_df = df[(df['Sex'] == 'female') & (df['Age'] > 20)]

print(filtered_df[["Name", "Sex", "Age"]])

avg_by_sex = df.groupby('Sex')['Age'].mean()
# print(avg_by_sex)

avg_female = avg_by_sex.get('female', None)
avg_male = avg_by_sex.get('male', None)

print("Средний возраст:")
print("женщин", avg_female)
print("мужчин", avg_male)

