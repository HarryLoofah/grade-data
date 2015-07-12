#!/usr/bin/env python

"""
grade-data
==========

A script for processing ELD grades from .csv files. This script does not focus
on individual student progress, but plots overall classroom trends.

The program reads a previously downloaded gradebook spreadsheet then converts
'number +/-' scores, standards based scores, and 'missing' or 'excused' values
to numeric values. Afterwards, scores will be processed so that growth data can
be observed via plotting. Also, program assumes input is .csv since this is the
only file download format available.
"""

__version__ = "1.0"

# imports
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Get / store .csv file and students' language level.
import_csv = raw_input("Enter the name of the .csv file to import: ")
lang_level = raw_input("Enter language level (single number) for class: ")
# Get teacher name.
teacher_name = raw_input("Enter teacher's name: ")
# Get current date. Format.
time = datetime.datetime.now()
now = time.strftime("%Y-%m-%d %H:%M")

def clean_data():
    '''
    Function cleans up data by stripping header lines, student names, and
    converting grades to numeric values. Returns a data frame ready to plot.
    '''
    # Eliminate header rows and remove column 0 which contains student names.
    df = pd.read_csv(import_csv, skiprows=2, header=None)
    df = df.drop(0, 1)
    # Drop columns if all values are NaN (i.e. no grades were entered)
    df = df.dropna(axis=1, how='all')
    # Replace "excused" and "missing" values with NaN.
    df = df.replace(("e", "m"), "NaN", regex=True)
    # Convert standards based grades (u, pp, p, a) to numerical grade based on
    # classroom language level.
    to_replace = ('u', 'pp', 'p', 'a')
    value = (
            (int(lang_level) - 1),
            (int(lang_level) - .5),
            (int(lang_level)),
            (int(lang_level) + .5),
            )
    df = df.replace(to_replace, value, regex=True)
    # Convert values from 'number +/-' to numerical (based on lang. level).
    # Use .3 for '+'s and .7 for '-'s (i.e. 2- == 1.7)
    pm_replace = ('1+', '2-', '2+', '3-', '3+', '4-', '4+', '5-', '5+', '6-')
    pm_values = (1.3, 1.7, 2.3, 2.7, 3.3, 3.7, 4.3, 4.7, 5.3, 5.7)
    df = df.replace(pm_replace, pm_values, regex=True)
    # Convert all dataframe values to float = clean dataframe
    df_clean = df.astype(float)
    return df_clean
def calculate_column_mean(df_clean):
    '''
    Calculate mean of each column (mean of each assignment's scores) and return.
    '''
    df_mean = df_clean.mean(axis=0)
    return df_mean
def plot_df(df_mean):
    '''
    Plot the mean.
    '''
    # Define font for title and labels.
    font = {'family' : 'sans',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 14,
            }
    # Create plot with title and labels.
    df_mean.plot(kind='bar')
    plt.title('Teacher: {} -- Created: {}'.format(teacher_name, now))
    plt.xlabel('Assignments', fontdict=font)
    plt.ylabel('Scores', fontdict=font)
    plt.show()

if __name__ == "__main__":  # This seems wrong, but couldn't make it work w/o.
    clean_data()
    calculate_column_mean(clean_data())
    plot_df(calculate_column_mean(clean_data()))
