#!/usr/bin/env python

# Author: Greg Aitkenhead <gregaitkenhead@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
A simple program for processing ELD grades from .csv files.

This program will first read the .csv file containing grades and then convert
the "number +/-" system used in ELD to a numeric score. Afterwards, scores will
be processed so that growth data can be observed. Also, program assumes input
is .csv.

Program will need to account for missing values, excused / missing assignments,
and convert "u through a" grades.
"""
__version__ = "0.2"

# imports
import pandas as pd

# Use pandas 'read_csv' to read 'extract.csv' without header rows.
df = pd.read_csv("extract.csv", sep=',', skiprows=2, header=None)

# Remove column with student names.
df = df.drop(0, 1)

# Add new column names based on len of assignments.
#df.columns = [col_list]


# Convert values from 'number +/-' to numerical and handle missing values.
