import pandas as pd
import numpy as np


def clean_graduate_data(data):
    cleaned_data = drop_columns(data, ['Sources'])
    cleaned_data = rename_column(cleaned_data, 'Full-Time Permanent Employment Rate', 'Employment Rate')
    cleaned_data = rename_column(cleaned_data, 'Gross Monthly Salary ($) Mean', 'Mean Salary')
    cleaned_data = rename_column(cleaned_data, 'Gross Monthly Salary ($) Median', 'Median Salary')
    cleaned_data = rename_column(cleaned_data, 'Gross Monthly Salary ($) 25th Percentile', '25th Percentile')
    cleaned_data = rename_column(cleaned_data, 'Gross Monthly Salary ($) 75th Percentile', '75th Percentile')
    cleaned_data['Mean Salary'] = cleaned_data['Mean Salary'].apply(remove_unwanted)
    cleaned_data['Median Salary'] = cleaned_data['Median Salary'].apply(remove_unwanted)
    cleaned_data['25th Percentile'] = cleaned_data['25th Percentile'].apply(remove_unwanted)
    cleaned_data['75th Percentile'] = cleaned_data['75th Percentile'].apply(remove_unwanted)

    # remove 0 values
    cleaned_data = cleaned_data[~(cleaned_data['Employment Rate'] <= 0)]

    return cleaned_data


def remove_unwanted(s):
    s = s.replace('$', '')
    return s.replace(',', '')


def get_data(data, file_type):
    excel_type = ['xls', 'xlsx']

    if file_type == "csv":
        data = pd.read_csv(data)

    if file_type in excel_type:
        data = pd.read_excel(data)

    return data


def get_data_by_school(data, school):
    result = data.loc[data['Institution'] == school]
    return result


def drop_columns(data, columns):
    data = data.drop(columns, axis=1)
    return data


def rename_column(data, column, name):
    data = data.rename(columns={column:name})
    return data


def handle_missing_vals(data, fill=''):
    if fill == '':
        data = data.dropna(how='all')

    else:
        data = data.fillna(fill)

    return data
