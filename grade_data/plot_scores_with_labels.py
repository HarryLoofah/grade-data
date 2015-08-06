#!/usr/bin/env python

"""
full_grade_data.py
==========

    This is a test script to processes ELD grades from CSV files and plot
    overall classroom trends. I'm working on incorporating more information
    the imported CSV file, especially dates associated with assignments.

    Like grade-data's "main.py", this script converts 'number +/-' scores and
    standards based scores to numeric values, and handles 'missing' or
    'excused' values.  The final product will still be a plot showing overall
    class or agregate student progress.

    :copyright: (c) 2015 by Greg Aitkenhead
    :license: MIT
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd

IMPORT_CSV = "extract.csv"
LANG_LEVEL = 3
TEACHER_NAME = "GA"


def clean_data(csv):
    ''' Takes a csv file (in this case "IMPORT_CSV") and removes unnecessary
        rows and columns. Returns a clean dataframe ready for plotting.
    '''
    # Read in gradebook data (IC download = csv file called "extract.csv")
    df = pd.read_csv(csv)

    # Drop the first column ("Unnamed: 0) as it contains students names which
    # won't be considered when ploting class averages.
    df = df.drop('Unnamed: 0', axis=1)
    # Drop first row under header row (each cell contains "100" as a value).
    df = df.drop(0)
    # Drop columns if all values are NaN (i.e. no grades were entered).
    df = df.dropna(axis=1, how='all')

    # Replace assignment label elements with consistent values.
    # This helps to clean up the mess with 2014/2015 gradebook values, but
    # should not be necessary (remove?) for 2015/2016 if assignments are
    # entered with abbreviated names.
    df = df.rename(columns=lambda x: x.replace("Unit", "U"))
    df = df.rename(columns=lambda x: x.replace("Week", "W"))
    df = df.rename(columns=lambda x: x.replace("Wk", "W"))
    df = df.rename(columns=lambda x: x.replace(" ", ""))

    # Shorten column labels to 4 characters + "...".
    df = df.rename(columns=lambda x: x[:4] + "...")

    # Replace "excused" and "missing" values with NaN.
    df = df.replace(("e", "m", "E", "M"), "NaN", regex=True)

    # Change standards based grades to numerical grade based on language level.
    to_replace = ('u', 'pp', 'p', 'a')
    new_value = (
        (int(LANG_LEVEL) - 1),
        (int(LANG_LEVEL) - .5),
        (int(LANG_LEVEL)),
        (int(LANG_LEVEL) + .5),
    )
    df = df.replace(to_replace, new_value, regex=True)

    # Convert values from 'number +/-' to numerical.
    pm_replace = ('1+', '2-', '2+', '3-', '3+', '4-', '4+', '5-', '5+', '6-')
    pm_values = (1.3, 1.7, 2.3, 2.7, 3.3, 3.7, 4.3, 4.7, 5.3, 5.7)
    df = df.replace(pm_replace, pm_values, regex=True)

    # Convert dataframe values to float.
    df = df.astype(float)

    # Find the mean value of all columns.
    df = df.mean(axis=0)

    return df


def main():
    """Plot the data using output from clean_data()."""
    # Clean the dataframe to plot.
    clean_df = clean_data(IMPORT_CSV)
    # Get today's date for the plot title.
    now = (datetime.datetime.now()).strftime("%m-%d-%Y")
    # Set the font for plot x and y labels.
    font = {
        'family':    'sans',
        'color':     'darkred',
        'weight':    'normal',
        'size':       14
    }

    # Plot the dataframe.
    clean_df.plot(kind='bar')
    plt.title('Teacher: {}  Created: {}'.format(TEACHER_NAME, now))
    plt.xlabel('Assignments', fontdict=font)
    plt.ylabel('Scores', fontdict=font)
    # Use to accomodate longer tick labels on the bottom of the plot.
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
