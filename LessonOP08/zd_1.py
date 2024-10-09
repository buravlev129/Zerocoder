
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список задач")
        
        # Создаем список задач
        self.tasks = []

        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Поле для ввода новой задачи
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=10)

        # Кнопка добавления задачи
        self.add_button = tk.Button(self.root, text="Добавить задачу", command=self.add_task)
        self.add_button.pack(pady=5)

        # Список задач с галочками
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack()

        # Кнопка удаления отмеченных задач
        self.delete_button = tk.Button(self.root, text="Удалить отмеченные задачи", command=self.delete_tasks)
        self.delete_button.pack(pady=5)

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            var = tk.BooleanVar()
            task = tk.Checkbutton(self.tasks_frame, text=task_text, variable=var)
            task.pack(anchor='w')
            self.tasks.append((task, var))
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Введите текст задачи перед добавлением.")

    def delete_tasks(self):
        for task, var in self.tasks:
            if var.get():  # Если задача отмечена
                task.pack_forget()
        # Удаляем отмеченные задачи из списка
        self.tasks = [t for t in self.tasks if not t[1].get()]

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

    #ttk.Treeview

if __name__ == "__main__":
    main()
