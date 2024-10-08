import tkinter as tk
from tkinter import ttk

from tasks import Task


class TaskForm:
    """
    Форма для ввода данных задачи
    """

    def __init__(self, parent, title=None):
        self.task: Task = None
        self._cancelled = False

        self.parent = parent
        self.title = title if title else "Task 1"

        r = tk.Toplevel(self.parent)
        self.root = r
        r.title(self.title)
        r.protocol("WM_DELETE_WINDOW", self.on_window_closing)

        r = self.root
        self.window_width = 400
        self.window_height = 200

        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width - self.window_width) // 2
        y = parent_y + (parent_height - self.window_height) // 2
        
        r.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        # r.geometry(f"{self.window_width}x{self.window_height}")
        r.resizable(tk.FALSE, tk.FALSE)

        r.grid_columnconfigure(0, weight=1)
        r.grid_columnconfigure(1, weight=1)
        r.grid_columnconfigure(2, weight=1)

        tk.Label(r, text="Параметры задачи", width=40, background="gray98").grid(row=0, column=1, columnspan=2, sticky="NW", padx=0, pady=5)

        tk.Label(r, text="ID:", width=40).grid(row=1, column=0, sticky="NW", padx=0, pady=1)
        self.txtId = tk.Entry(r, width=30) #, state='readonly')
        self.txtId.grid(row=1, column=1, columnspan=1, sticky="NW", padx=3, pady=2)

        tk.Label(r, text="Name:", width=40).grid(row=2, column=0, sticky="NW", padx=0, pady=1)
        self.txtName = tk.Entry(r, width=70)
        self.txtName.grid(row=2, column=1, columnspan=1, sticky="NW", padx=3, pady=2)

        tk.Label(r, text="Descr:", width=40).grid(row=3, column=0, sticky="NW", padx=0, pady=1)
        self.txtDesc = tk.Text(r, width=70, height=3)
        self.txtDesc.grid(row=3, column=1, columnspan=1, sticky="NW", padx=3, pady=2)

        tk.Label(r, text="Status:", width=40).grid(row=4, column=0, sticky="NW", padx=0, pady=1)
        self.cbo = ttk.Combobox(r, width=26, values=Task.get_supported_status_list())
        self.cbo.grid(row=4, column=1, columnspan=1, sticky="NW", padx=3, pady=2)
        self.cbo.current(0)

        frame = ttk.Frame(r, height=30, padding=1, borderwidth=0, relief="flat")
        frame.grid(row=5, column=1, columnspan=2, sticky="WE", padx=3, pady=2)

        btnSave = tk.Button(frame, text="Сохранить", command=self.save_data)
        btnSave.grid(row=0, column=0, sticky="NW", padx=3, pady=3)
        btnCancel = tk.Button(frame, text="Отмена", command=self.cancel)
        btnCancel.grid(row=0, column=1, sticky="NW", padx=3, pady=3)


    @property
    def window(self):
        return self.root

    @property
    def is_cancelled(self):
        return self._cancelled


    def set_task(self, task: Task):
        self.txtId.insert(0, str(task.id))
        self.txtName.insert(0, task.name)
        self.txtDesc.insert(0.0, task.description)
        self.cbo.set(task.status)


    def save_data(self):
        self._cancelled = False
        t = Task()
        t.id = self.txtId.get()
        t.name = self.txtName.get()
        t.description = self.txtDesc.get(0.0, "end")
        t.status = self.cbo.get()
        self.task = t
        self.root.destroy()


    def cancel(self):
        self._cancelled = True
        self.root.destroy()


    def on_window_closing(self):
        # if messagebox.askokcancel("Выход", "Вы действительно хотите закрыть окно?"):
        # self.save_data_on_exit()
        self.root.destroy()        
    

    def mainloop(self):
        self.root.mainloop()


