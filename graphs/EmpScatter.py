from itertools import cycle
import seaborn as sns
import mplcursors


def display_emp_scatter(df, axes):
    # Set the plot styles using seaborn lib
    sns.set_style('whitegrid')
    sns.set_style('ticks')

    # Define the columns for the x and y coordinates
    x_column = 'Year of Survey'
    y_column = 'Employment Rate'

    # Change through marker styles for different qualifications since got too many alr
    markers = cycle(['o', 's', 'D', '^', 'x'])
    for qualification in df['Qualification'].unique():
        marker = next(markers)
        qualification_data = df[df['Qualification'] == qualification]
        axes.scatter(qualification_data[x_column], qualification_data[y_column], marker=marker, label=qualification)

    # Setting plot title and labels
    axes.set_title('Employment Rate vs Year of Survey', fontsize=16)
    axes.set_xlabel(x_column, fontsize=12)
    axes.set_ylabel(y_column, fontsize=12)

    # Setting plot limits
    axes.set_xlim(df[x_column].min() - 1, df[x_column].max() + 1)
    axes.set_ylim(df[y_column].min() - 1, df[y_column].max() + 1)

    # Enable mplcursors for interactive data labels
    # This one is for the hover over label effect cos the legend too clunky
    mplcursors.cursor(hover=True)
