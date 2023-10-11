import matplotlib.pyplot as plt
from helpers.data_helper import get_data_by_school


def display_emp_pie(df, school, axes):
    sch_df = get_data_by_school(df, school)
    years = sch_df['Year of Survey'].unique()
    emp_rate = []

    # Store the average employment rate of all courses in that year
    for year in years.tolist():
        specific_year_df = sch_df.loc[sch_df['Year of Survey'] == year]
        year_emp_rate = specific_year_df['Employment Rate'].tolist()
        avrg_year_emp = sum(year_emp_rate)/len(year_emp_rate)

        emp_rate.append(avrg_year_emp)

    # Create the pie chart based on school
    wedges, texts, autotexts = axes.pie(
        emp_rate,
        labels=years,
        autopct=lambda x: str(round(x * sum(emp_rate), 1)) + '%',
        startangle=90,
        pctdistance=0.81,
        explode=list(map(lambda _: 0.05, range(len(years))))

    )

    # Set title of pie chart
    axes.set_title(f'Overview of average employment Rate in {school}', fontsize=14)
