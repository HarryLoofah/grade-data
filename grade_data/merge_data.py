#!/usr/bin/env python

"""
merge_data.py
=============

    This script merges a set of gradebook spreadsheets into a single .csv file
    that can be used with grade-data's main.py. Assumes folder of spreadsheets
    is stored in a directory other than 'grade_data'.

    :copyright: (c) 2015 by Greg Aitkenhead
    :license: MIT
"""
import pandas as pd
import os


files = !ls *.csv # IPython magic
d = concat([read_csv(f, index_col=0, header=None, axis=1) for f in files], keys=files)


#def main():
#    """Read in CSV files from directory. While reading in remove header rows.
#    This step also creates dataframes for each CSV file.
#    """
#    # Ask user for file and ID information and set current time (to use with plot).
#    IMPORT_DIR = raw_input("Enter the name of the directory with CSV files: ")
#
#    path = '.'
#
#    df = None
#    dfList=[]
#    for filename in [IMPORT_DIR+x for x in os.listdir(path)]:
#        dfList.append(pd.read_csv(filename))
#
#    df=pd.concat(dfList)
#    df.to_csv('out.csv', mode='w')

# Remove first column (contains student names).

# Concatenate dataframes.

# Save final product to same directory as "main.py".



if __name__ == "__main__":
    main()
