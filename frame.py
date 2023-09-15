from tkinter import Frame, Tk, Menu, BOTH, END, Text, filedialog
from pandastable import Table
from helper import clean_graduate_data
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.parent.title('Avian Stat')

        frame = Frame(self.parent)
        frame.pack(fill=BOTH)

        data = pd.read_csv('./Universities Graduate Employment Survey.csv')

        data = clean_graduate_data(data)
        pt = Table(frame, dataframe=data)
        pt.editable = True
        pt.show()

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Open...', command=self.open_file)
        menubar.add_cascade(menu=file_menu, label='File')

        edit_menu = Menu(menubar)
        menubar.add_cascade(menu=edit_menu, label='Edit')

    def open_file(self):
        file_types = [('CSV files', '*.csv')]
        file_path = filedialog.askopenfile(filetypes=file_types)
