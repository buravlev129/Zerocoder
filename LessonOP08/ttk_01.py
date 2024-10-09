import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Пример TreeView с иконками")
        self.root.geometry("500x100")

        # Создаем Treeview
        columns = ("Состояние", "Задача", "Примечание")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        
        # Определяем заголовки колонок
        self.tree.heading("Состояние", text="Состояние")
        self.tree.heading("Задача", text="Задача")
        self.tree.heading("Примечание", text="Примечание")
        
        # Определяем ширину колонок
        self.tree.column("Состояние", width=50)
        self.tree.column("Задача", width=150)
        self.tree.column("Примечание", width=200)
        
        # Размещаем Treeview
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Загрузка иконки
        self.icon = Image.open("A.png")  # Убедитесь, что иконка 32x32 пикселя
        self.icon = self.icon.resize((32, 32)) #, Image.ANTIALIAS)
        self.icon_tk = ImageTk.PhotoImage(self.icon)
        
        # Создаем стиль для отображения иконки
        style = ttk.Style()
        style.element_create('Treeitem.icon', 'image', self.icon_tk)
        style.layout('Treeview.Item', [
            ('Treeitem.padding', {
                'sticky': 'nswe',
                'children': [
                    ('Treeitem.icon', {'side': 'left', 'sticky': ''}),
                    ('Treeitem.text', {'side': 'left', 'sticky': ''}),
                ]
            })
        ])
        
        # Добавление данных в Treeview
        self.tree.insert("", "end", values=("1", "Задача 1", "Описание задачи 1"))
        self.tree.insert("", "end", values=("В работе", "Задача 2", "Описание задачи 2"))
        self.tree.insert("", "end", values=("Ожидание", "Задача 3", "Описание задачи 3"))
        self.tree.insert("", "end", values=("2", "Задача 1", "Описание задачи 1"))
        self.tree.insert("", "end", values=("В работе", "Задача 2", "Описание задачи 2"))
        self.tree.insert("", "end", values=("Ожидание", "Задача 3", "Описание задачи 3"))
        self.tree.insert("", "end", values=("3", "Задача 1", "Описание задачи 1"))
        self.tree.insert("", "end", values=("В работе", "Задача 2", "Описание задачи 2"))
        self.tree.insert("", "end", values=("Ожидание", "Задача 3", "Описание задачи 3"))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
