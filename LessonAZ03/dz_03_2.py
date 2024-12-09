import numpy as np
import matplotlib.pyplot as plt

N = 100  # Количество точек
x = np.random.rand(N)
y = np.random.rand(N)

plt.scatter(x, y)

plt.xlabel('X Axis')
plt.ylabel('Y Axis')

plt.title('Диаграмма рассеяния случайных данных')
plt.show()