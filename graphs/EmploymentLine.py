import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as Figure
from helpers.data_helper import get_data_by_school
matplotlib.use('TkAgg')


def Display_line_graph(df, school, course, axes):

    course_data = get_data_by_school(df, school, course)

    year = course_data['Year of Survey'].unique()
    employ = course_data['Employment Rate']
    print(course_data['Qualification'])
    print(employ)
    axes.set_ylabel('Employment Rate')
    axes.set_xlabel('Years')
    axes.plot(year, employ)
