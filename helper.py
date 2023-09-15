import pandas as pd


def clean_graduate_data(data):
    cleaned_data = drop_columns(data, ['Sources'])

    return cleaned_data


def get_data(data, file_type):
    if file_type == "csv":
        data = pd.read_csv(data)

    return data


def drop_columns(data, columns):
    data = data.drop(columns, axis=1)
    return data


def rename_column(data, column, name):
    data = data.rename(columns={column:name})
    return data
