from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from tkinter import filedialog
from pandastable import Table
from helpers.data_helper import clean_graduate_data, get_data, get_data_by_school, drop_columns
from helpers.ui_helper import create_combobox, create_figure_canvas
from graphs.CourseBar import displayCourseBar
from graphs.salaryPieChart import display_salary_pie
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.view_data_win = None
        self.users_data = None
        self.data_table = None
        self.init_ui()

    def init_ui(self):
        self.parent.title('Avian Stat')

        width = self.parent.winfo_screenwidth()
        height = self.parent.winfo_screenheight()

        self.parent.geometry('%dx%d' % (width, height))
        self.parent.state('zoomed')

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Open...', command=self.open_file)
        file_menu.add_command(label='Save as')
        menubar.add_cascade(menu=file_menu, label='File')

        graph_frame = Frame(self.parent)
        graph_frame.pack(fill=BOTH)

        data = pd.read_csv('./Universities Graduate Employment Survey.csv')

        data = clean_graduate_data(data)
        data.head()
        df = pd.DataFrame(data)

        scrollbar = Scrollbar(self.parent)
        scrollbar.pack(side=RIGHT, fill=Y)

        schools = data['Institution'].unique().tolist()

        top_frame = Frame(self.parent)
        top_frame.pack(fill=BOTH)

        Label(top_frame, text="Select an institution: ", font=("Arial", 16)).pack()

        school_combo = create_combobox(top_frame, schools, 'readonly')
        school_combo.pack()

        sch_df = get_data_by_school(df, schools[0])

        Label(top_frame, text="Select a year: ", font=("Arial", 16)).pack()

        self.year_combo = create_combobox(top_frame, sch_df['Year of Survey'].unique().tolist(), 'readonly')
        self.year_combo.pack()

        pie_figure, pie_axes, pie_figure_canvas = create_figure_canvas((16, 8), self.parent)

        # pack graph into window
        pie_figure_canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        display_salary_pie(df, school_combo.get(), self.year_combo.get(), pie_axes)

        def pie_school_change(event):
            # Change pie chart values when school and year is selected
            selected_school = school_combo.get()
            filtered_df = get_data_by_school(df, selected_school)

            self.year_combo['values'] = filtered_df['Year of Survey'].unique().tolist()
            selected_year = self.year_combo.get()

            if selected_year not in self.year_combo['values']:
                selected_year = self.year_combo['values'][0]

            self.year_combo.set(selected_year)

            pie_axes.clear()
            display_salary_pie(df, selected_school, selected_year, pie_axes)
            pie_figure_canvas.draw()

        school_combo.bind('<<ComboboxSelected>>', pie_school_change)
        self.year_combo.bind('<<ComboboxSelected>>', pie_school_change)

        top_frame = Frame(self.parent, height=30)
        top_frame.pack(fill=BOTH, pady=50)

        (Label(top_frame, text='Please select school and course to compare with', font=('Aerial', 20, 'bold'))
         .pack(pady=25))

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

        bar_figure, bar_axes, bar_figure_canvas = create_figure_canvas((10, 6), self.parent)

        # pack graph into window
        bar_figure_canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        displayCourseBar(df, school_combo.get(), self.course_combo.get(), compared_school_combo.get(),
                         self.compared_course_combo.get(), bar_axes)

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

            bar_axes.clear()
            displayCourseBar(df, selected_school, selected_course, selected_comparison, selected_compared_course, bar_axes)
            bar_figure_canvas.draw()

        # Change bars when school or course change
        school_combo.bind('<<ComboboxSelected>>', school_change)
        compared_school_combo.bind('<<ComboboxSelected>>', school_change)
        self.course_combo.bind('<<ComboboxSelected>>', school_change)
        self.compared_course_combo.bind('<<ComboboxSelected>>', school_change)

    def refresh_table(self):
        # Redraw table on change
        self.data_table.model.df = self.users_data
        self.data_table.redraw()

    def open_file(self):
        file_types = [('CSV files', '*.csv'), ('Excel files', '*.xls, xlsx')]

        # open file dialog
        file_path = filedialog.askopenfilename(filetypes=file_types)

        # get file name
        file_name = file_path.split('/')[-1]

        # get file type
        uploaded_file_type = file_name.split('.')[1]

        self.users_data = get_data(file_path, uploaded_file_type)

        self.view_data_win = Toplevel(self.parent)
        self.view_data_win.title(file_name)
        self.view_data_win.state('zoomed')

        menubar = Menu(self.view_data_win)
        self.view_data_win.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Save as')
        file_menu.add_command(label='Close', command=self.view_data_win.destroy)
        menubar.add_cascade(menu=file_menu, label='File')

        edit_menu = Menu(menubar)
        edit_menu.add_command(label='Drop columns', command=self.drop_col)
        menubar.add_cascade(menu=edit_menu, label='Edit')

        frame = Frame(self.view_data_win)
        frame.pack(fill=BOTH, expand=1)

        # Display data with pandastable
        self.data_table = Table(frame)
        self.data_table.model.df = self.users_data
        self.data_table.show()

    def drop_col(self):
        # Create new window for dropping columns
        drop_col_win = Toplevel(self.view_data_win)
        drop_col_win.title('Drop columns')
        drop_col_win.geometry('300x700')

        drop_col_win.resizable(False, False)

        frame = LabelFrame(drop_col_win, text="Select columns to drop", padx=20, pady=20, font='Arial 16')
        frame.pack(pady=20, padx=10)

        checkbox_vars = []

        # Create checkboxes based on column names
        for col in self.users_data.columns:
            var = IntVar()
            checkbox = Checkbutton(frame, text=col, anchor='w', width=200, font='Arial 16',
                                   variable=var)
            checkbox_vars.append((var, col))
            checkbox.pack()

        def drop():
            cols_to_drop = []

            for chk_var, col in checkbox_vars:
                # Store col name if checkbox is checked
                if chk_var.get() == 1:
                    cols_to_drop.append(col)

            # Drop columns if any checked
            if cols_to_drop:
                self.users_data = drop_columns(self.users_data, cols_to_drop)
                self.refresh_table()

            # Close the drop col window
            drop_col_win.destroy()

        drop_button = Button(frame, text='Drop columns', font='Arial 16', command=drop)
        drop_button.pack(fill=X)
