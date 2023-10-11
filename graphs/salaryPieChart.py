from helpers.data_helper import get_data_by_school
import matplotlib
from matplotlib.widgets import Slider


# Create a function to generate the pie chart based on user selection
def display_salary_pie(df, school, year, axes):
    # Strip spaces from user input
    school = school.replace(" ", "")

    # Convert the year to an integer
    year = int(year)

    # Filter the DataFrame based on the user's input
    filtered_df = df[(df['Institution'].str.replace(" ", "") == school) & (df['Year of Survey'] == year)]

    # Group by 'Faculty' and calculate the average salary for each faculty in the filtered data
    faculty_salary_mean = filtered_df.groupby('Faculty')['Mean Salary'].mean()

    # Create a pie chart for the filtered data with a larger size
    wedges, texts, autotexts = axes.pie(faculty_salary_mean, labels=faculty_salary_mean.index, autopct='%1.1f%%',
                                        startangle=140, textprops={'fontsize': 14})

    axes.set_title(f'Distribution of Mean Salary by Faculty at {school} ({year})', y=1.08, fontsize=16)
    axes.axis('equal')

    # Make the Faculty labels and autopct text larger
    for label, autotext in zip(texts, autotexts):
        label.set_fontsize(14)
        autotext.set_fontsize(14)


def display_faculty_bar(df, school, year, faculty, axes):
    bars_displayed = 4

    sch_df = get_data_by_school(df, school)
    specific_year_df = sch_df.loc[sch_df['Year of Survey'] == int(year)]

    courses = specific_year_df.loc[specific_year_df['Faculty'] == faculty, 'Qualification'].tolist()
    salary = specific_year_df.loc[specific_year_df['Faculty'] == faculty, 'Mean Salary'].tolist()

    def update_bar_with_slider(pos):
        # position of slider
        pos = int(pos)

        # clear plot to display certain number of bars
        axes.clear()

        if pos + bars_displayed > len(courses):
            n = len(courses) - pos

        else:
            n = bars_displayed

        # slices the data according to position and num of bars to display and displays it
        displayed_courses = courses[pos:pos+n]
        displayed_salary = salary[pos:pos+n]

        bars = axes.bar(displayed_courses, displayed_salary)

        axes.set_xlabel('Qualification', fontsize=14)
        axes.set_ylabel('Mean Salary', fontsize=14)

        modified_labels = []
        max_words = 3

        for label in axes.get_xticklabels():
            text = label.get_text()
            words = text.split()
            if len(words) > max_words:
                # Insert line breaks (newline) into the label
                modified_label = '\n'.join([' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)])
                modified_labels.append(modified_label)

            else:
                modified_labels.append(text)

        axes.set_xticklabels(modified_labels)

        axes.set_title(f'Average Gross Monthly Salary by Qualification for {faculty} in {year}', fontsize=16)
        if len(bars) < 1:
            axes.set_title(f'No data for {faculty} in {year}', fontsize=16, color='red')

        # Adding labels with values (including "$") above the bars
        for bar in bars:
            height = bar.get_height()
            axes.annotate(f'${height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),  # 3 points vertical offset
                          textcoords="offset points",
                          ha='center', fontsize=12)

    slider_ax = matplotlib.pyplot.axes([0.18, 0.05, 0.55, 0.03], facecolor="skyblue")
    slider = Slider(slider_ax, 'Courses', 0, len(courses) - bars_displayed, valinit=0,
                    valstep=1, track_color='green')
    slider.valtext.set_visible(False)

    # update bar graph as slider is moved
    slider.on_changed(update_bar_with_slider)

    # Display initial bars
    update_bar_with_slider(0)
    return slider
