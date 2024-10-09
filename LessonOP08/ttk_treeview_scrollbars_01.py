import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Пример TreeView с иконками")
        
        # Создаем контейнер для Treeview и Scrollbar
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview
        columns = ("Состояние", "Задача", "Примечание")
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        
        # Определяем заголовки колонок
        self.tree.heading("Состояние", text="Состояние")
        self.tree.heading("Задача", text="Задача")
        self.tree.heading("Примечание", text="Примечание")
        
        # Определяем ширину колонок
        self.tree.column("Состояние", width=100)
        self.tree.column("Задача", width=150)
        self.tree.column("Примечание", width=200)
        
        # Создаем вертикальный скроллбар
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Размещаем Treeview и Scrollbar
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Настраиваем контейнер для изменения размеров
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Загрузка иконки
        self.icon = Image.open("A.png")  # Убедитесь, что иконка 32x32 пикселя
        self.icon = self.icon.resize((32, 32)) #, Image.ANTIALIAS)
        self.icon_tk = ImageTk.PhotoImage(self.icon)
        
        # Добавление данных в Treeview
        for i in range(1, 11):  # Добавим несколько строк, чтобы был виден скроллинг
            self.tree.insert("", "end", values=(f"Состояние {i}", f"Задача {i}", f"Описание задачи {i}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
