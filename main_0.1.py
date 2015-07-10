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

# imports
import csv, sys

__version__ = "0.1"

# Code used to read 'extract.csv' into copy 'cleaned.csv' without header rows.
with open("extract.csv", "rb") as infile, open("cleaned.csv", "wb") as outfile:
    reader = csv.reader(infile)
    next(reader, None) # skip first header row
    next(reader, None) # skip second header row
    writer = csv.writer(outfile)

    # Convert values from 'number +/-' to numerical and handle missing values.
    try:
        for row in reader:
            # Work on set of values in each row, converting to numerical:
            # Note -- should I use regex?
            for grade in row[1:]: # look at grades, skip std names (column 1)
                grade = str(grade)
                test = grade.replace("p", "Works!")
                print test
            # Process rows and write to outfile (skipping column 1 std names).
            writer.writerow(row[1:])

    # Catch and report any errors.
    except csv.Error as e:
         sys.exit('file %s, line %d: %s' % (infile, reader.line_num, e))
