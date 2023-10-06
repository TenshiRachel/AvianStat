from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from tkinter import filedialog
from pandastable import Table
from helpers.data_helper import clean_graduate_data, get_data, get_data_by_school
from helpers.ui_helper import create_combobox, create_figure_canvas
from graphs.CourseBar import displayCourseBar
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
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

        top_frame = Frame(self.parent, height=30)
        top_frame.pack(fill=BOTH, pady=50)

        graph_frame = Frame(self.parent)
        graph_frame.pack(fill=BOTH)

        data = pd.read_csv('./Universities Graduate Employment Survey.csv')

        data = clean_graduate_data(data)
        data.head()
        df = pd.DataFrame(data)

        scrollbar = Scrollbar(self.parent)
        scrollbar.pack(side=RIGHT, fill=Y)

        (Label(top_frame, text='Please select school and course to compare with', font=('Aerial', 20, 'bold'))
         .pack(pady=25))

        schools = data['Institution'].unique().tolist()

        # Combo box for universities
        school_combo = create_combobox(top_frame, schools, 'readonly')
        school_combo.pack(side=LEFT, padx=(100, 50))

        compared_school_combo = create_combobox(top_frame, schools, 'readonly')
        compared_school_combo.pack(side=RIGHT, padx=(50, 100))

        sch_df = get_data_by_school(df, schools[0])

        # Combobox for courses in the university
        self.course_combo = create_combobox(top_frame, sch_df['Qualification'].unique().tolist(), 'readonly',
                                            70)
        self.course_combo.pack(side=LEFT, padx=(0, 20))

        self.compared_course_combo = create_combobox(top_frame, sch_df['Qualification'].unique().tolist(),
                                                     'readonly', 70)
        self.compared_course_combo.pack(side=RIGHT, padx=(20, 0))

        figure, axes, figure_canvas = create_figure_canvas((10, 6), self.parent)

        # pack graph into window
        figure_canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        displayCourseBar(df, school_combo.get(), self.course_combo.get(), compared_school_combo.get(),
                         self.compared_course_combo.get(), axes)

        def school_change(event):
            selected_school = school_combo.get()
            selected_comparison = compared_school_combo.get()

            sch_df_filter = get_data_by_school(df, selected_school)
            compared_df = get_data_by_school(df, selected_comparison)

            # Set value of course combobox to qualifications of selected university
            self.course_combo['values'] = sch_df_filter['Qualification'].unique().tolist()
            selected_course = self.course_combo.get()
            self.compared_course_combo['values'] = compared_df['Qualification'].unique().tolist()
            selected_compared_course = self.compared_course_combo.get()

            # Change to first course of changed university if university changes
            if selected_course not in self.course_combo['values']:
                selected_course = self.course_combo['values'][0]
            if selected_compared_course not in self.compared_course_combo['values']:
                selected_compared_course = self.compared_course_combo['values'][0]

            # Set value of course combobox to first course value
            self.course_combo.set(selected_course)
            self.compared_course_combo.set(selected_compared_course)

            axes.clear()
            displayCourseBar(df, selected_school, selected_course, selected_comparison, selected_compared_course, axes)
            figure_canvas.draw()

        # Change bars when school or course change
        school_combo.bind('<<ComboboxSelected>>', school_change)
        compared_school_combo.bind('<<ComboboxSelected>>', school_change)
        self.course_combo.bind('<<ComboboxSelected>>', school_change)
        self.compared_course_combo.bind('<<ComboboxSelected>>', school_change)

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
