import pandas as pd
import numpy as np
import re
import pytest

def func1(x: pd.DataFrame, column_name: str):
    '''
    filter out rows if values in the given column are null values

    :param x (pd.DataFrame): Tabular data as a Pandas Dataframe
    :param column_name (string): Name of the column to filter on

    :return: output pd.DataFrame
    '''

    # axis = 0, drop rows wich contain missing values
    # how = 'any', if there is any null values, the axis specified row/column is dropped(row in this case)
    # subset = [column_name], specified the column where to check null values 
    filtered_data = x.dropna(axis = 0, how = 'any', subset=[column_name])
    return filtered_data

def clean_function (string: str):
    '''
    Remove all characters that appear between parentheses

    :param string (str): string to clean
    
    :return: cleaned string
    '''
    
    return re.sub(r'\([^)]*\)', '', string).replace('(', '').replace(')', '').strip()
    
def func2(x: pd.DataFrame):
    '''
    select and return only rows in which if Cause category is equal to Traffic Control then Cause Subcategory must be equal to Others or Police Controlled.
    Moreover the function must “clean” the Million Plus Cities column of the selected rows removing all characters that appear between parentheses. 
    Remove the parentheses also.

    :param x (pd.DataFrame: Tabular data as a Pandas DataFrame

    :return: output pd.DataFrame
    '''
    
    #With this condition are selected only the rows that have  Cause category equal to Traffic Control and then Cause Subcategory equal to Others or Police Controlled /
    # 'isin' Pandas function check whether each element in the Dataframe is contained on input array column values
    # another DataFrame is created because otherwise an error is reported (SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame)
    filtered_data = pd.DataFrame(x[(x['Cause category'] == 'Traffic Control') & (x['Cause Subcategory'].isin(['Others','Police Controlled']))])
    
    # in the end the 'Milion Plus Cities' column is cleaned applying a clean_function
    filtered_data['Million Plus Cities'] = filtered_data['Million Plus Cities'].apply(lambda x: clean_function(x))

    return filtered_data

def test_Func1(x:pd.DataFrame):
    #Secondly is checked if the application of func1, filter out the rows with null values
    column_name = 'Count'
    #numbers of elements null in the original dataframe
    n_null_element_original = x[column_name].isnull().sum()
    
    filtered_f1 = func1(x,column_name)
    #numbers of elements null in the filtered dataframe
    n_null_element_filtered = filtered_f1[column_name].isnull().sum()
    
    #is checked that the number of filtered element is lower or equal to the original
    #and the number of null elements in the filtered DataFrame is equal to 0
    assert n_null_element_filtered <= n_null_element_original
    assert n_null_element_filtered == 0

def test_Func2(x:pd.DataFrame):
    #numbers of values that have '(' character  in Million Plus Cities column in the original dataframe
    not_cleaned_dataframe_dirty_values = x['Million Plus Cities'].apply(lambda x : '(' in x).sum()
    
    cleaned_dataframe = func2(x)
    #numbers of values that have '(' character  in Million Plus Cities column in the filtered dataframe
    cleaned_dataframe_dirty_values = cleaned_dataframe['Million Plus Cities'].apply(lambda x : '(' in x).sum()

    #is checked that the number of filtered element is lower or equal to the original
    #and the number of null elements in the filtered DataFrame is equal to 0
    assert cleaned_dataframe_dirty_values <= not_cleaned_dataframe_dirty_values
    assert cleaned_dataframe_dirty_values == 0

if __name__ == "__main__":
    dataframe = pd.read_csv("../data/indian_accident.csv")
    test_Func1(dataframe)
    test_Func2(dataframe)
    print("Test completed")