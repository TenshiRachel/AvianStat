from tkinter import *
from tkinter import filedialog
from tkinter.font import nametofont, Font

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

import matplotlib
matplotlib.use('TkAgg')
from pandastable import Table
from helpers.data_helper import (clean_graduate_data, get_data, get_data_by_school, drop_columns, rename_column,
                                 handle_missing_vals)
from helpers.ui_helper import create_combobox, create_figure_canvas, show_toast
from graphs.CourseBar import displayCourseBar
from graphs.salaryPieChart import display_salary_pie
import pandas as pd


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        # Default font for menu items
        self.menu_font = Font(family='Arial', size=14)
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

        # Default font for widgets
        nametofont('TkDefaultFont').configure(size=16)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        file_menu = Menu(menubar)
        file_menu.add_command(label='Open...', command=self.open_file, font=self.menu_font)
        menubar.add_cascade(menu=file_menu, label='File')

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
            displayCourseBar(df, selected_school, selected_course, selected_comparison, selected_compared_course,
                             bar_axes)
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
        file_menu.add_command(label='Save as', font=self.menu_font)
        file_menu.add_command(label='Close', command=self.view_data_win.destroy, font=self.menu_font)
        menubar.add_cascade(menu=file_menu, label='File')

        edit_menu = Menu(menubar)
        edit_menu.add_command(label='Drop columns', command=self.drop_col, font=self.menu_font)
        edit_menu.add_command(label='Rename columns', command=self.rename_col, font=self.menu_font)

        handling_menu = Menu(edit_menu)
        edit_menu.add_cascade(menu=handling_menu, label='Handle missing values', font=self.menu_font)
        handling_menu.add_command(label='Fill null values', command=self.fill_na, font=self.menu_font)
        handling_menu.add_command(label='Drop null value rows', command=self.drop_na, font=self.menu_font)

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
        drop_col_win.geometry('500x500')

        drop_col_win.resizable(False, False)

        canvas = Canvas(drop_col_win)
        canvas.pack(fill=BOTH, expand=True)

        # Make canvas scrollable based on content
        scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        frame.pack(fill=BOTH, expand=True)

        canvas.create_window((0, 0), window=frame, anchor=NW)

        label_frame = LabelFrame(frame, text="Select columns to drop")
        label_frame.pack(fill=BOTH, expand=True, padx=20, pady=(20, 60))

        checkbox_vars = []

        # Create checkboxes based on column names
        for col in self.users_data.columns:
            var = IntVar()
            checkbox = Checkbutton(label_frame, text=col, anchor='w', width=20,
                                   variable=var)
            checkbox_vars.append((var, col))
            checkbox.pack()

        # Update content on scoll
        label_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

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
                show_toast('Column(s) dropped successfully!', SUCCESS)

            else:
                show_toast('At least one column must be selected', DANGER)

        drop_button = ttkb.Button(label_frame, text='Drop columns', command=drop, bootstyle=SUCCESS)
        drop_button.pack(fill=X, pady=10)

    def rename_col(self):
        # Create new window for renaming columns
        rename_col_win = Toplevel(self.view_data_win)
        rename_col_win.title('Rename columns')
        rename_col_win.geometry('500x500')

        rename_col_win.resizable(False, False)

        canvas = Canvas(rename_col_win)
        canvas.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        frame.pack(fill=BOTH, expand=True)

        canvas.create_window((0, 0), window=frame, anchor=NW)

        label_frame = LabelFrame(frame, text="Rename columns", padx=20)
        label_frame.pack(fill=BOTH, expand=True, pady=(20, 60), padx=10)

        entries = []

        for col in self.users_data.columns:
            textbox = Entry(label_frame, font='Arial 16')
            # Insert column names as values in textbox
            textbox.delete(0, END)
            textbox.insert(0, col)

            textbox.pack(pady=15)
            # Store entries to retrieve values later
            entries.append(textbox)

        label_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

        def rename():
            renames = {}
            # Create renames dict based on entries
            for i, entry in enumerate(entries):
                renames[self.users_data.columns[i]] = entry.get()

            # Check for blank entries
            if '' in renames.values():
                show_toast('No blanks are allowed', DANGER)

            else:
                # Rename the columns and update the table
                self.users_data = rename_column(self.users_data, renames)
                self.refresh_table()

                rename_col_win.destroy()
                show_toast('Column(s) renamed successfully!', SUCCESS)

        rename_button = ttkb.Button(label_frame, text='Rename columns', command=rename, bootstyle=SUCCESS)
        rename_button.pack(fill=X, pady=10)

    def fill_na(self):
        # Create new window for filling na columns
        fill_na_win = Toplevel(self.view_data_win)
        fill_na_win.title('Fill null values')
        fill_na_win.geometry('400x200')

        fill_na_win.resizable(False, False)

        # Let user enter value they want to replace null with
        label_frame = LabelFrame(fill_na_win, text="Enter value to fill nulls", padx=20)
        label_frame.pack(fill=BOTH, expand=True, pady=20, padx=10)

        textbox = Entry(label_frame, font='Arial 16')
        textbox.pack(pady=10)

        def fill():
            # Get value of textbox
            fill_value = textbox.get()

            # Check for blank entry
            if fill_value != '':
                self.users_data = handle_missing_vals(self.users_data, fill_value)
                self.refresh_table()

                fill_na_win.destroy()
                show_toast('Null values filled!', SUCCESS)

            else:
                show_toast('Please enter a value!', DANGER)

        fill_button = ttkb.Button(label_frame, text='Fill null values', command=fill, bootstyle=SUCCESS)
        fill_button.pack(fill=X, pady=10)

    def drop_na(self):
        # Create new window for filling na columns
        drop_na_win = Toplevel(self.view_data_win)
        drop_na_win.title('Drop null values')
        drop_na_win.geometry('450x300')

        drop_na_win.resizable(False, False)

        label_frame = LabelFrame(drop_na_win, text="Select method of dropping", padx=20)
        label_frame.pack(fill=BOTH, expand=True, pady=20, padx=10)

        radio = IntVar()

        # Let user choose between methods
        any_radio = ttkb.Radiobutton(label_frame, text='Drop rows where any value is null', variable=radio, value=0)
        all_radio = ttkb.Radiobutton(label_frame, text='Drop rows where all values are null', variable=radio, value=1)

        any_radio.pack(pady=10, anchor=W)
        all_radio.pack(pady=10, anchor=W)

        def drop():
            # Check user choice and drop according to it
            if not radio.get():
                self.users_data = handle_missing_vals(self.users_data)
            else:
                self.users_data = handle_missing_vals(self.users_data, any_col=False)

            self.refresh_table()

            drop_na_win.destroy()
            show_toast('Rows with null dropped', SUCCESS)

        drop_button = ttkb.Button(label_frame, text='Drop null values', command=drop, bootstyle=SUCCESS)
        drop_button.pack(fill=X, pady=10)
