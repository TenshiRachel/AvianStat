import matplotlib
import tkinter as tk
import numpy as np
from helper import get_data_by_school


matplotlib.use('TkAgg')


def displayCourseBar(dataframe, school, canvas, axes):
    sch_df = get_data_by_school(dataframe, school)

    meanSalary = sch_df['Mean Salary']
    employmentRate = sch_df['Employment Rate']
    years = sch_df['Year of Survey']
    courses = sch_df['Qualification']
    print(len(courses.unique()))
    # redraw graph
    axes.clear()

    create_axes(axes, courses, meanSalary)
    canvas.draw()

    # pack graph into window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def create_axes(axes, courses, meanSalary):
    # create the barchart
    axes.barh(courses, np.asarray(meanSalary, float), color='green', label='Mean Salary ($)')
    # axes.barh(courses, employmentRate, width, color='blue', label='Employment rate')
    axes.set_title('Salary and Employment rate over the years in different courses')
    axes.set_ylabel('Course')

    axes.legend()
