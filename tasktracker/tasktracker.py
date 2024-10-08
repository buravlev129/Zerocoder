"""
Простое приложение для управления задачами, таск-трекер
"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import resicons as rex
from appstate import AppState
from jsondb import JsonDb
from ttkbars import Toolbar, ToolbarPlaceholder, ToolbarSeparator, Statusbar3
from frmtask import TaskForm
from tasks import Task



class TaskTracker:
    """
    Приложение для управления задачами
    """

    app_icon = """
    R0lGODlhEAAQAPIGAAAAAP//AAAA//8AqgD//4aGhv///wAAACH5BAEAAAAALAAAAAAQABAAAANCCLrcUDBKqWYkpO
    BSra+GIYxkOT6hGQTCehapKaNiaN8iLRhD7/c5WA13E+h4P18wRSw+ILuk0rjYNVMM2czBXSQAADs=
    """

    def __init__(self, title=None, theme=None):
        self.title = title if title else "Task Tracker"
        self.theme = theme if theme else "vista"
        self.data_file = "tracker-db.json"
        self.something_changed = False

        self.state = AppState()
        self.state.load()

        r = tk.Tk()
        self.root = r
        r.title(self.title)
        r.withdraw()
        try:
            self._eimg =tk.PhotoImage(data=self.app_icon)
            r.option_add('*tearOff', tk.FALSE)
            r.tk.call('wm', 'iconphoto', r._w, self._eimg)

            r.protocol("WM_DELETE_WINDOW", self.on_window_closing)

            self.window_width = self.state.get_int("TaskTracker.frmMain.width", 500)
            self.window_height = self.state.get_int("TaskTracker.frmMain.height", 300)
            self.window_top = self.state.get_int("TaskTracker.frmMain.top", 0)
            self.window_left = self.state.get_int("TaskTracker.frmMain.left", 0)
            self.theme = self.state.get_value("TaskTracker.theme", "vista")
            self.initialize_UI()
        finally:
            r.deiconify()

    @property
    def window(self):
        return self.root

    def mainloop(self):
        self.root.mainloop()


    #region Инициализация графического интерфейса

    def initialize_UI(self):
        r = self.root
        # r.grid_rowconfigure(0, weight=1)
        # r.grid_columnconfigure(0, weight=1)        

        stl = ttk.Style(r)
        stl.theme_use(self.theme)

        screen_width = r.winfo_screenwidth()
        screen_height = r.winfo_screenheight()      
        center_x = int((screen_width - self.window_width) / 2)
        center_y = int((screen_height - self.window_height) / 2)

        x = center_x if self.window_left <= 0 else self.window_left
        y = center_y if self.window_top <= 0 else self.window_top

        r.minsize(400, 400)
        #r.maxsize(1200, 1000)
        r.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        r.resizable(tk.TRUE, tk.TRUE)

        self.init_toolbar()
        self.init_taskframe()


    def init_toolbar(self):
        tb = Toolbar(self.root)
        tb.pack_top()

        #b = tb.AddButtonEmb("bt_conn", embdata=rex.conn01_gif, command=self.change_theme)
        #b.config(state=tk.DISABLED)
        ho = ToolbarPlaceholder(tb)
        b = tb.AddButtonEmb("bt_new", embdata=rex.doc_new01_gif, command=self.btn_add_new_click)
        b = tb.AddButtonEmb("bt_edit", embdata=rex.doc_edit02_gif, command=self.btn_edit_click)
        b = tb.AddButtonEmb("bt_drop", embdata=rex.row_drop_gif, command=self.btn_drop_click)
        sep = ToolbarSeparator(tb)
        b = tb.AddButtonEmb("bt_save", embdata=rex.save1_gif, command=self.btn_save_click)
        # sep = ToolbarSeparator(tb)
        # b = tb.AddButtonEmb("bt_tools", embdata=rex.tools_01_gif, command=self.btn_add_new_click)
        # b.config(state=tk.DISABLED)

        sb = Statusbar3(self.root)
        sb.set_db_status(self.data_file)

    #endregion

    #region Работа с таблицей TreeView

    def init_taskframe(self):
        frame = ttk.Frame(self.root, padding=1, borderwidth=0, relief="flat")
        frame.pack(fill='both', expand=True)

        s = ttk.Style()
        s.configure("Treeview.Heading", font=(None, 10))
        
        tv = ttk.Treeview(frame, column=("ID", "Name", "Description", "Status"), show="headings"
                          , displaycolumns=("ID", "Name", "Description", "Status"), selectmode = 'browse')
        tv.pack(fill='both', expand=True)

        self.tvtable = tv
        # tv.column("#0", width=20, stretch=False, anchor="w")
        tv.column("ID", width=40, stretch=False, anchor="w")
        tv.column("Name", width=140, stretch=True, anchor="w")
        tv.column("Description", width=240, stretch=True, anchor="w")
        tv.column("Status", width=60, stretch=False, anchor="w")
        
        tv.heading('ID', text='ИД')
        tv.heading('Name', text='Название задачи')
        tv.heading('Description', text='Описание')
        tv.heading('Status', text='Статус')

        tv.tag_configure("tg_new", foreground="black")
        tv.tag_configure("tg_work", foreground="navy", background="azure")
        tv.tag_configure("tg_done", foreground="gray", font=(None, 9, "overstrike"))

        tv.bind('<<TreeviewSelect>>', self.on_select_row)
        # tv.insert("", "end", values=(10, "Задача 10", "Новое задание", "New"), tags="tg_new")
        # tv.insert("", "end", values=(12, "Задача 12", "Новое задание", "New"), tags="tg_new")
        # tv.insert("", "end", values=(15, "Задача 15", "Новое задание", "In work"), tags="tg_work")
        # tv.insert("", "end", values=(16, "Задача 16", "Новое задание", "Done"), tags="tg_done")
        # tv.insert("", "end", values=(23, "Задача 23", "Новое задание", "In work"), tags="tg_work")

        self.load_data_file()


    def on_select_row(self, event):
        """
        Выбор записи в таблице
        """
        # t = self.get_selected_task()
        pass


    def get_selected_task(self):
        """
        Возвращает текущую задачу в таблице (если что-то выбрано)
        """
        tv = self.tvtable
        if len(tv.selection()) > 0:
            selected_item = tv.selection()[0]
            row = tv.item(selected_item)
            values = row["values"]

            t = Task()
            t.id = values[0]
            t.name = values[1]
            t.description = values[2]
            t.status = values[3]
            return t
        return None


    def insert_task(self, t: Task):
        """
        Вставляет переданную задачу в таблицу
        """
        tv = self.tvtable
        tv.insert("", "end", values=(t.id, t.name, t.description, t.status), tags=(t.tag,))


    def drop_task(self):
        """
        Удаляет текущую задачу из таблицы
        """
        tv = self.tvtable
        if len(tv.selection()) > 0:
            selected_item = tv.selection()[0]
            if selected_item:
                tv.delete(selected_item)
                self.something_changed = True


    def add_new_task(self):
        """
        Добавление новой задачи
        """
        try:
            frm = TaskForm(self.root, "Новая задача")
            frm.window.grab_set()
            self.root.wait_window(frm.window)

            if not frm.is_cancelled:
                self.insert_task(frm.task)
                self.something_changed = True

        except Exception as ex:
            print(str(ex))


    def edit_task(self):
        """
        Редактирование задачи
        """
        try:
            t = self.get_selected_task()
            if not t:
                messagebox.showwarning(title=self.title, message="Выберите запись в таблице")
                return

            frm = TaskForm(self.root, t.name)
            frm.set_task(t)
            frm.window.grab_set()
            self.root.wait_window(frm.window)

            if not frm.is_cancelled:
                tv = self.tvtable
                selected_item = tv.selection()[0]
                tv.item(selected_item, values=frm.task.get_tuple())
                tv.item(selected_item, tags=(frm.task.tag,))
                self.something_changed = True

        except Exception as ex:
            print(str(ex))


    def load_data_file(self):
        """
        Загрузка json файла в таблицу
        """
        tv = self.tvtable
        for item_id in tv.get_children():
            tv.delete(item_id)

        db = JsonDb(filename=self.data_file)
        data = db.load_data()
        for values in data:
            t = Task.from_array(values)
            tag = (t.tag,)
            tv.insert('', 'end', values=values, tags=tag)


    def save_data_file(self):
        """
        Сохранение содержимого таблицы в json файл
        """
        db = JsonDb(filename=self.data_file)
        
        data = []
        tv = self.tvtable
        for item_id in tv.get_children():
            item = tv.item(item_id)
            data.append(item['values'])
        
        db.write_data(data)


    #endregion

    #region Обработка событий окна и нажатия кнопок

    def on_window_closing(self):
        if self.something_changed:
            ret = messagebox.askyesnocancel("Выход", "Данные на форме были изменены.\nСохранить изменения?")
            if ret is None:
                return
            
            if ret:
                self.save_data_file()

        self.save_window_settings()
        self.root.destroy()
            
    
    def save_window_settings(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        top = self.root.winfo_y()
        left = self.root.winfo_x()

        self.state.set_value("TaskTracker.frmMain.width", width)
        self.state.set_value("TaskTracker.frmMain.height", height)
        self.state.set_value("TaskTracker.frmMain.top", top)
        self.state.set_value("TaskTracker.frmMain.left", left)

        self.state.save()


    def btn_add_new_click(self):
        self.add_new_task()

    def btn_edit_click(self):
        self.edit_task()

    def btn_drop_click(self):
        self.drop_task()

    def btn_save_click(self):
        if not self.something_changed:
            return
        self.save_data_file()

    def change_theme(self):
        pass

    #endregion






if __name__ == "__main__":

    try:
        app = TaskTracker()
        app.mainloop()
    except Exception as ex:
        print(str(ex))
