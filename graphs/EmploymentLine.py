import matplotlib
from helpers.data_helper import get_data_by_school
matplotlib.use('TkAgg')


def display_emp_line(df, school, course, compared_school, compared_course, axes):

    course_data = get_data_by_school(df, school, course)
    compared_course_data = get_data_by_school(df, compared_school, compared_course)

    year = course_data['Year of Survey'].unique().tolist()
    compared_year = compared_course_data['Year of Survey'].unique().tolist()

    all_year = sorted(set(year) | set(compared_year))
    employ = course_data['Employment Rate']
    compared_employ = compared_course_data['Employment Rate']

    axes.set_ylabel('Employment Rate', fontsize=14)
    axes.set_xlabel('Years', fontsize=14)

    axes.set_xticks(all_year)

    axes.set_ylim(0, 1)

    if len(course_data) > 1:
        axes.set_title('Comparison of trend in employment rate over the years for %s in %s and %s in %s' %
                       (course, school, compared_course, compared_school))

        axes.plot(year, employ, label=course)
        axes.plot(compared_year, compared_employ, label=compared_course)

    else:
        axes.set_title('Insufficient data from %s to plot graph' % course, color='red')
