import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap
from helpers.data_helper import get_data_by_school


matplotlib.use('TkAgg')


def displayCourseBar(dataframe, school, course, other_school, other_course, axes):
    # TODO: Annotate bars with salary and no data if value is 0
    sch_course_df = get_data_by_school(dataframe, school, other=course)
    compared_df = get_data_by_school(dataframe, other_school, other=other_course)

    years = sch_course_df['Year of Survey'].unique()
    compared_years = compared_df['Year of Survey'].unique()

    # Get unique years
    all_years = sorted(set(years) | set(compared_years))

    salaries = []
    compared_salaries = []

    for year in all_years:
        # Get salary according to particular year
        salary1 = sch_course_df.loc[sch_course_df['Year of Survey'] == year, 'Mean Salary'].values
        salary2 = compared_df.loc[compared_df['Year of Survey'] == year, 'Mean Salary'].values

        # Append 0 if the year is not present in the dataframe
        if not salary1:
            salary1 = [0]
        if not salary2:
            salary2 = [0]

        # Store salary attributed to that year
        salaries.append(salary1[0])
        compared_salaries.append(salary2[0])

    x_pos = np.arange(len(all_years))
    bar_pos = []

    width = 0.7  # Width of each individual bar
    group_spacing = 1  # Adjust this value for spacing between groups
    bar_colors = plt.cm.viridis(np.linspace(0, 0.5, len(all_years)))
    compared_bar_colors = plt.cm.viridis(np.linspace(0.5, 1, len(all_years)))

    for i, (salary, compared_salary, year) in enumerate(zip(salaries, compared_salaries, all_years)):
        offset = width * (i - (len(all_years) - 1) - group_spacing/2)
        compared_offset = width * (i - (len(all_years) - 1) + group_spacing/2)

        # Store position of grouped bars to position x ticks
        bar_pos.append((x_pos[i]*2 + offset + compared_offset)/2)

        axes.bar(x_pos[i] + offset, salary, width, label='%s - %s' % (school, course) if i == 0 else '',
                 color=bar_colors[i], align='center')

        axes.bar(x_pos[i] + compared_offset, compared_salary, width,
                 label='%s - %s' % (other_school, other_course) if i == 0 else '',
                 color=compared_bar_colors[i], align='center')

    # Set labels
    axes.set_xlabel('Year')
    axes.set_ylabel('Mean Salary')

    # Prevent x labels overlap
    axes.set_xticks(bar_pos)
    axes.set_xticklabels(all_years, rotation=30, ha='center')

    # Legend to show what school and course
    axes.legend()

    # Title of graph
    axes.set_title('\n'.join(wrap('Comparison of salary over the years between %s in %s and %s in %s', 50)) %
                   (course, school, other_course, other_school))
