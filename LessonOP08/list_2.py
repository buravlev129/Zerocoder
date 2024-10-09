import tkinter as tk

class ScrollableChecklist:
    def __init__(self, root):
        self.root = root
        self.root.title("Список с галками и скроллингом")

        # Создаем фрейм для холста и скроллбара
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        # Создаем холст
        self.canvas = tk.Canvas(frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Добавляем скроллбар
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Создаем внутренний фрейм, который будет содержать Checkbutton
        self.checklist_frame = tk.Frame(self.canvas)
        self.checklist_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Добавляем внутренний фрейм в холст
        self.canvas.create_window((0, 0), window=self.checklist_frame, anchor="nw")

        # Привязываем скроллбар к холсту
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Создаем список задач
        self.tasks = []
        self.task_vars = []

        # Демонстрация: добавляем несколько задач
        for i in range(20):  # Пример с 20 задачами
            self.add_task(f"Задача {i+1}")

    def add_task(self, task_text):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(self.checklist_frame, text=task_text, variable=var)
        cb.pack(anchor='w')
        self.tasks.append(cb)
        self.task_vars.append(var)

def main():
    root = tk.Tk()
    app = ScrollableChecklist(root)
    root.geometry("300x200")  # Устанавливаем размер окна
    root.mainloop()

if __name__ == "__main__":
    main()
