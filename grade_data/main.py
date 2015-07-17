#!/usr/bin/env python

"""
grade-data
==========

    This script processes ELD grades from CSV files and plots overall
    classroom trends.

    It converts 'number +/-' scores and standards based scores to numeric
    values, and handles 'missing' or 'excused' values.  Final product is a
    plot showing class progress.

    :copyright: (c) 2015 by Greg Aitkenhead
    :license: MIT
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Ask user for file and ID information and set current time (to use with plot).
IMPORT_CSV = raw_input("Enter the name of the CSV file to import: ")
LANG_LEVEL = raw_input("Enter language level (single number) for class: ")
TEACHER_NAME = raw_input("Enter teacher's name or initials: ")

# Read in CSV file after user input.  The CSV files from the gradebook report
# contain a top header row with assignment names followed by a row containing
# all zeros.  It is easiest to remove these rows when reading in the CSV file.
# All other manipulation of the dataframe will take place in 'clean_data()'.
DF = pd.read_csv(IMPORT_CSV, skiprows=2, header=None)


def clean_data(dataframe):
    """Cleans data by stripping header lines, student names, and converting
    various types of grades to numeric values.  Returns a plotable data frame.
    """
    # Remove column 0 (which contains student names).
    dataframe = dataframe.drop(0, 1)
    # Drop columns if all values are NaN (i.e. no grades were entered).
    dataframe = dataframe.dropna(axis=1, how='all')
    # Replace "excused" and "missing" values with NaN.
    dataframe = dataframe.replace(("e", "m", "E", "M"), "NaN", regex=True)

    # Change standards based grades to numerical grade based on language level.
    to_replace = ('u', 'pp', 'p', 'a')
    value = (
        (int(LANG_LEVEL) - 1),
        (int(LANG_LEVEL) - .5),
        (int(LANG_LEVEL)),
        (int(LANG_LEVEL) + .5),
    )
    dataframe = dataframe.replace(to_replace, value, regex=True)

    # Convert values from 'number +/-' to numerical.
    pm_replace = ('1+', '2-', '2+', '3-', '3+', '4-', '4+', '5-', '5+', '6-')
    pm_values = (1.3, 1.7, 2.3, 2.7, 3.3, 3.7, 4.3, 4.7, 5.3, 5.7)
    dataframe = dataframe.replace(pm_replace, pm_values, regex=True)

    # Convert dataframe values to float.
    dataframe = dataframe.astype(float)
    # Find the mean value of all columns.
    dataframe = dataframe.mean(axis=0)

    return dataframe


def main():
    """Plot the data using output from clean_data()."""
    # Clean the dataframe to plot.
    clean_dataframe = clean_data(DF)
    # Get today's date for the plot title.
    now = (datetime.datetime.now()).strftime("%m-%d-%Y")
    # Set the font for plot x and y labels.
    font = {
        'family':    'sans',
        'color':     'darkred',
        'weight':    'normal',
        'size':       14
    }

    # Create the plot.
    clean_dataframe.plot(kind='bar')
    plt.title('Teacher: {}  Created: {}'.format(TEACHER_NAME, now))
    plt.xlabel('Assignments', fontdict=font)
    plt.ylabel('Scores', fontdict=font)

    plt.show()


if __name__ == "__main__":
    main()
