
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


TOOLBAR_HEIGHT = 26
TOOLBAR_SEP_HEIGHT = 20
STATUSBAR_HEIGHT = 26
STATUSBAR_SEP_HEIGHT = 20



class Toolbar(ttk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(master=parent, height=26, border=0, relief=GROOVE, **kw)
        self.parent = parent
        self.buttons = {}
        

    def pack_top(self):
        self.pack(side=TOP, fill=X)

    def grid_top(self, row=0, column=0, colspan=1):
        self.grid(row=row, column=column, columnspan=colspan)

    # btn.config(state=DISABLED)
    # btn.config(state=NORMAL)
    def AddButton_xxx(self, key, pictureFile, command):
        if key in self.buttons.keys():
            raise KeyError("Key is already added" % key)
        imgConn = Image.open(pictureFile)
        eimgConn = ImageTk.PhotoImage(imgConn)
        b = ttk.Button(self, image=eimgConn, command=command) #, relief=GROOVE
        b.image = eimgConn
        b.pack(side=LEFT, padx=2, pady=2)
        self.buttons[key] = b
        return b

    def AddButtonGif(self, key, pictureFile, command):
        if key in self.buttons.keys():
            raise KeyError("Key is already added" % key)
        eimg = PhotoImage(file=pictureFile)
        b = ttk.Button(self, image=eimg, command=command) # , relief=FLAT
        b.image = eimg
        b.pack(side=LEFT, padx=2, pady=2)
        self.buttons[key] = b
        return b

    def AddButtonEmb(self, key, embdata, command, side=LEFT):
        if key in self.buttons.keys():
            raise KeyError("Key is already added" % key)
        eimg = PhotoImage(data=embdata)
        b = ttk.Button(self, image=eimg, command=command) # , relief=FLAT
        b.image = eimg
        b.pack(side=side, padx=0, pady=2)
        self.buttons[key] = b
        return b

    def Hide(self):
        self.pack_forget()
    def Show(self, before=None):
        self.pack(side=TOP, before=before, fill=X)


class ToolbarSeparator(ttk.Frame):
    """Разделитель для кнопок тулбара"""
    def __init__(self, parent, **kw):
        super().__init__(master=parent, height=TOOLBAR_SEP_HEIGHT, width=3, relief=GROOVE, **kw)
        self.parent = parent
        self.pack(side=LEFT, padx=5, pady=0)


class ToolbarPlaceholder(ttk.Frame):
    """Плейсхолдер в тулбаре"""
    def __init__(self, parent, **kw):
        super().__init__(master=parent, height=TOOLBAR_SEP_HEIGHT, width=10, relief=FLAT, **kw)
        self.parent = parent
        self.pack(side=LEFT, padx=5, pady=0)


class Statusbar3(ttk.Frame):

    def __init__(self, parent, msg1=None, msg2=None, **kw):
        self.strip_height = 26
        super().__init__(master=parent, height=STATUSBAR_HEIGHT, relief=GROOVE, **kw)
        self.pack(side=BOTTOM, fill=X, padx=0, pady=0)
        self.panels = {}
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.stt_text = Label(self, text=msg1, relief=FLAT, anchor=W)
        self.stt_text.grid(row=0, column=0, sticky=W+E, padx=2, pady=2)
        self.sep1 = ttk.Frame(self, width=3, height=STATUSBAR_SEP_HEIGHT, relief=GROOVE)
        self.sep1.grid(row=0, column=1, sticky=W+E, padx=0, pady=0)
        self.stt_db = Label(self, text=msg2, relief=FLAT, anchor=W)
        self.stt_db.grid(row=0, column=2, sticky=W, padx=2, pady=2)
        self.stt_db["text"] = " "*20

    def set_db_status(self, text):
        self.stt_db["text"] = text if text else " "*20
