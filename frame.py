from tkinter import *
from tkinter import filedialog, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from pandastable import Table
from helper import clean_graduate_data, get_data
from graphs.CourseBar import displayCourseBar
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.parent.title('Avian Stat')
        self.parent.geometry('1400x800')

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Open...', command=self.open_file)
        file_menu.add_command(label='Save as')
        menubar.add_cascade(menu=file_menu, label='File')

        edit_menu = Menu(menubar)
        edit_menu.add_command(label='Drop columns', command=self.drop_col)
        menubar.add_cascade(menu=edit_menu, label='Edit')

        frame = Frame(self.parent)
        frame.pack(fill=BOTH, expand=1)

        data = pd.read_csv('./Universities Graduate Employment Survey.csv')

        data = clean_graduate_data(data)
        data.head()
        df = pd.DataFrame(data)

        schools = data['Institution'].unique()
        sv = StringVar()

        # combo box for universities
        comboBox = ttk.Combobox(self.parent, textvariable=sv)
        comboBox['values'] = schools.tolist()
        comboBox['state'] = 'readonly'
        comboBox.current(0)
        comboBox.pack()

        # create a figure
        figure = Figure(figsize=(10, 20), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas)

        # create axes
        axes = figure.add_subplot()

        displayCourseBar(df, schools.tolist()[0], figure_canvas, axes)

        def school_change(event):
            displayCourseBar(df, sv.get(), figure_canvas, axes)

        # execute plot change on school change
        comboBox.bind('<<ComboboxSelected>>', school_change)

        pt = Table(frame)
        pt.model.df = data

        pt.show()

    def open_file(self):
        file_types = [('CSV files', '*.csv'), ('Excel files', '*.xls, xlsx')]

        # open file dialog
        file_path = filedialog.askopenfilename(filetypes=file_types)

        # get file name
        file_name = file_path.split('/')[-1]

        # get file type
        uploaded_file_type = file_name.split('.')[1]

        data = get_data(file_path, uploaded_file_type)

        frame = Frame(self.parent)
        frame.pack(fill=BOTH, expand=1)
        pt = Table(frame)
        pt.model.df = data
        pt.show()

    def drop_col(self):
        # open new window
        drop_col_win = Toplevel(self.parent)
        drop_col_win.title('Drop columns')
        drop_col_win.geometry('300x500')
        pass
