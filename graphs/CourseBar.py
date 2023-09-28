import matplotlib
from matplotlib.widgets import Slider
import numpy as np
from helper import get_data_by_school


matplotlib.use('TkAgg')

# number of bars to display
bars_displayed = 12


def displayCourseBar(dataframe, school, axes):
    sch_df = get_data_by_school(dataframe, school)

    meanSalary = sch_df['Mean Salary']
    years = sch_df['Year of Survey']
    courses = sch_df['Qualification']

    def update_bar_with_slider(pos):
        # position of slider
        pos = int(pos)

        # clear plot to display certain number of bars
        axes.clear()

        if pos + bars_displayed > len(courses.unique()):
            n = len(courses.unique()) - pos

        else:
            n = bars_displayed

        # slices the data according to position and num of bars to display and displays it
        displayed_courses = courses[pos:pos+n]
        displayed_salary = meanSalary[pos:pos+n]

        # create the barchart
        axes.bar(displayed_courses, np.asarray(displayed_salary, float),
                 color='green', label='Mean Salary ($)', align='edge')

        # prevent overlap of labels
        matplotlib.pyplot.setp(axes.get_xticklabels(), rotation=30, ha='center')

        # title of graph
        axes.set_title('Salary over the years in different courses in ' + school)

        # show graph legend
        axes.legend()

    slider_ax = matplotlib.pyplot.axes([0.18, 0.05, 0.55, 0.03], facecolor="skyblue")
    slider = Slider(slider_ax, 'Courses', 0, len(courses.unique()) - bars_displayed, valinit=0,
                    valstep=1, track_color='grey')

    # update bar graph as slider is moved
    slider.on_changed(update_bar_with_slider)

    # hide slider value
    slider.valtext.set_visible(False)

    # start at pos 0 and init bar graph
    update_bar_with_slider(0)

    return slider
