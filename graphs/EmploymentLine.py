import matplotlib
from helpers.data_helper import get_data_by_school
matplotlib.use('TkAgg')


def display_emp_line(df, school, course, axes):

    course_data = get_data_by_school(df, school, course)

    year = course_data['Year of Survey'].unique().tolist()
    year = [int(i) for i in year]
    employ = course_data['Employment Rate']

    axes.set_ylabel('Employment Rate')
    axes.set_xlabel('Years')

    axes.set_xticks(year)

    axes.set_ylim(0, 1)

    if len(course_data) > 1:
        axes.set_title('Trend in employment rate over the years for %s in %s' % (course, school))

        axes.plot(year, employ)

    else:
        axes.set_title('Insufficient data from %s to plot graph' % course, color='red')
