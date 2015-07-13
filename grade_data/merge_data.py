#!/usr/bin/env python

"""
merge_data.py
=============

A script for processing ELD grades from .csv files.  This script does not focus
on individual student progress, but plots overall classroom trends.

The program merges a previously downloaded set of gradebook spreadsheets into a
single .csv file that can be used with grade-data's main.py. Assumes folder of
spreadsheets is store in a directory other than 'grade_data'.
"""

__version__ = "1.0"

# imports
