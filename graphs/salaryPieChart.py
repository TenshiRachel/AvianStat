
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

    axes.set_title(f'Distribution of Average Salary by Faculty at {school} ({year})', y=1.08, fontsize=16)
    axes.axis('equal')

    # Make the Faculty labels and autopct text larger
    for label, autotext in zip(texts, autotexts):
        label.set_fontsize(14)
        autotext.set_fontsize(14)



