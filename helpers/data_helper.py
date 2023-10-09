import pandas as pd
import numpy as np


def clean_graduate_data(data):
    cleaned_data = drop_columns(data, ['Sources'])
    renames = {'Full-Time Permanent Employment Rate': 'Employment Rate',
               'Gross Monthly Salary ($) Mean': 'Mean Salary',
               'Gross Monthly Salary ($) Median': 'Median Salary',
               'Gross Monthly Salary ($) 25th Percentile': '25th Percentile',
               'Gross Monthly Salary ($) 75th Percentile': '75th Percentile'}

    # Rename columns to simpler names
    cleaned_data.rename(columns=renames, inplace=True)

    # Convert digit related columns to float type
    cleaned_data[['Mean Salary', 'Median Salary', '25th Percentile', '75th Percentile']] = (
        cleaned_data[['Mean Salary', 'Median Salary', '25th Percentile', '75th Percentile']].applymap(convert_to_float))

    # remove 0 values
    cleaned_data = cleaned_data[~(cleaned_data['Employment Rate'] <= 0)]
    cleaned_data.sort_values(by='Year of Survey', inplace=True)

    return cleaned_data


def convert_to_float(s):
    s = s.replace('$', '')
    return float(s.replace(',', ''))


def get_data(data, file_type):
    excel_type = ['xls', 'xlsx']

    if file_type == "csv":
        data = pd.read_csv(data)

    if file_type in excel_type:
        data = pd.read_excel(data)

    data_with_nan = data.mask(data == '')

    return data_with_nan


def get_data_by_school(data, school, other=''):
    if other == '':
        result = data.loc[data['Institution'] == school]
    else:
        result = data.loc[(data['Institution'] == school) & (data['Qualification'] == other)]
    return result


def drop_columns(data, columns):
    data = data.drop(columns=columns, axis=1)
    return data


def rename_column(data, renames):
    data = data.rename(columns=renames, inplace=True)
    return data


def handle_missing_vals(data, fill='', any_col=True):
    if fill == '':
        if any_col:
            data = data.dropna(how='any')
        else:
            data = data.dropna(how='all')

    else:
        data = data.fillna(fill)

    return data
