#!/usr/bin/env python

"""
grade-data
==========

A script for processing ELD grades from .csv files.  This script does not focus
on individual student progress, but plots overall classroom trends.

The program reads a previously downloaded gradebook spreadsheet then converts
'number +/-' scores and standards based scores to numeric values, and handles
'missing' or 'excused' values.  Afterwards, scores will be processed so that
growth data can be observed via plotting.  Program assumes input is .csv.
"""

__version__ = "1.0"

import datetime
import matplotlib.pyplot as plt
import pandas as pd

IMPORT_CSV = raw_input("Enter the name of the .csv file to import: ")
LANG_LEVEL = raw_input("Enter language level (single number) for class: ")
TEACHER_NAME = raw_input("Enter teacher's name or initials: ")
TIME = datetime.datetime.now()
NOW = TIME.strftime("%Y-%m-%d %I:%M")

def clean_data():
    '''
    Cleans data by stripping header lines, student names, and converting various
    types of grades to numeric values.  Returns a data frame ready to plot.
    '''
    # Import .csv and eliminate header rows.
    df = pd.read_csv(IMPORT_CSV, skiprows=2, header=None)
    # Remove column 0 (which contains student names).
    df = df.drop(0, 1)
    # Drop columns if all values are NaN (i.e. no grades were entered).
    df = df.dropna(axis=1, how='all')
    # Replace "excused" and "missing" values with NaN.
    df = df.replace(("e", "m", "E", "M"), "NaN", regex=True)

    # Change standards based grades to numerical grade based on language level.
    to_replace = ('u', 'pp', 'p', 'a')
    value = (
        (int(LANG_LEVEL) - 1),
        (int(LANG_LEVEL) - .5),
        (int(LANG_LEVEL)),
        (int(LANG_LEVEL) + .5),
        )
    df = df.replace(to_replace, value, regex=True)

    # Convert values from 'number +/-' to numerical.
    pm_replace = ('1+', '2-', '2+', '3-', '3+', '4-', '4+', '5-', '5+', '6-')
    pm_values = (1.3, 1.7, 2.3, 2.7, 3.3, 3.7, 4.3, 4.7, 5.3, 5.7)
    df = df.replace(pm_replace, pm_values, regex=True)

    df = df.astype(float)

    return df

def calculate_column_mean(df):
    df_mean = df.mean(axis=0)
    return df_mean

def plot_df(df_mean):

    font = {'family' : 'sans',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 14,}

    df_mean.plot(kind='bar')
    plt.title('Teacher: {} -- Created: {}'.format(TEACHER_NAME, NOW))
    plt.xlabel('Assignments', fontdict=font)
    plt.ylabel('Scores', fontdict=font)

    plt.show()

if __name__ == "__main__":
    clean_data()
    calculate_column_mean(clean_data())
    plot_df(calculate_column_mean(clean_data()))
