from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from tkinter import filedialog, ttk
from pandastable import Table
from helper import clean_graduate_data, get_data, get_data_by_school
from graphs.CourseBar import displayCourseBar
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.course_combo = None
        self.init_ui()

    def init_ui(self):
        self.parent.title('Avian Stat')

        width = self.parent.winfo_screenwidth()
        height = self.parent.winfo_screenheight()

        self.parent.geometry('%dx%d' % (width, height))

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

        scrollbar = Scrollbar(self.parent)
        scrollbar.pack(side=RIGHT, fill=Y)

        (Label(self.parent, text='Please select school and course to compare with', font=('Aerial', 14, 'bold'))
         .pack(pady=15))

        schools = data['Institution'].unique()

        # Combo box for universities
        school_combo = ttk.Combobox(self.parent, values=schools.tolist(), state='readonly')
        school_combo.current(0)
        school_combo.pack()

        sch_df = get_data_by_school(df, schools.tolist()[0])

        # Combobox for courses in the university
        self.course_combo = ttk.Combobox(self.parent, values=sch_df['Qualification'].unique().tolist(),
                                         state='readonly', width=70)
        self.course_combo.current(0)
        self.course_combo.pack()

        # create figure and axes
        figure, axes = plt.subplots(figsize=(10, 6))
        figure.subplots_adjust(bottom=0.3)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, master=self.parent)

        # pack graph into window
        figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self.parent)

        displayCourseBar(df, school_combo.get(), self.course_combo.get(), axes)

        def school_change(event):
            selected_school = school_combo.get()

            sch_df_filter = get_data_by_school(df, selected_school)

            # Set value of course combobox to qualifications of selected university
            self.course_combo['values'] = sch_df_filter['Qualification'].unique().tolist()
            selected_course = self.course_combo.get()

            # Change to first course of changed university if university changes
            if selected_course not in self.course_combo['values']:
                selected_course = self.course_combo['values'][0]

            # Set value of course combobox to first course value
            self.course_combo.set(selected_course)
            axes.clear()
            displayCourseBar(df, selected_school, selected_course, axes)
            figure_canvas.draw()

        # execute plot change on school change
        school_combo.bind('<<ComboboxSelected>>', school_change)
        self.course_combo.bind('<<ComboboxSelected>>', school_change)

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
