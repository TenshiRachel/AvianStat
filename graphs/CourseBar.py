import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from helper import get_data_by_school


matplotlib.use('TkAgg')


def displayCourseBar(dataframe, school, course, axes):
    # TODO: compare with other graph
    sch_course_df = get_data_by_school(dataframe, school, other=course)

    # Create pivot dataframe and drop NaN values from salaries
    grouped_df = sch_course_df.groupby('Year of Survey')['Mean Salary'].apply(int).reset_index()

    years = grouped_df['Year of Survey']
    salaries = grouped_df['Mean Salary']

    x_pos = np.arange(len(grouped_df))
    bar_pos = []
    width = 0.5  # Width of each individual bar
    group_spacing = 0.2  # Adjust this value for spacing between groups
    bar_colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

    for i, (salary, year) in enumerate(zip(salaries, years)):
        offset = width * (i - (len(years) - 1)/2)

        # Store position of bars to position x ticks
        bar_pos.append(x_pos[i] + offset)

        axes.bar(x_pos[i] + offset, salary, width, label=str(year),
                 color=bar_colors[i], align='center')

    # Set labels
    axes.set_xlabel('Year')
    axes.set_ylabel('Mean Salary')

    # Prevent x labels overlap
    axes.set_xticks(bar_pos)
    axes.set_xticklabels(years, rotation=30, ha='center')

    # Year legend
    axes.legend(years, ncols=3)

    # Title of graph
    axes.set_title('Salary over the years for %s in %s' % (course, school))
