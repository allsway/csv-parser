#!/usr/bin/env python

import sys
import csv
import re
import pandas
import datetime

def read_csv(file):
    # drop blank rows when reading in
    df = pandas.read_csv(file, na_values=[' ', ''],error_bad_lines=False,
        skip_blank_lines=True)
    checked_column_names = check_header(df.columns.values)
    df.columns = checked_column_names
    # cleaning all string columns of newline characters, quotes, and bad characters
    for column in df:
        if df[column].dtype == 'object':
            df[column] = df[column].map(lambda x: clean_string(x))
    df = find_dupes(df)
    df.to_csv('corrected_' + str(datetime.datetime.now().strftime("%Y-%m-%d") +  file  )
        , index=False)

# Removes bad characters from string fields
def clean_string(address):
    address = address.replace('"','')
    address = address.replace("'",'')
    address  = address.replace('\r\n',', ')
    return address

# Find and drop duplicate rows
def find_dupes(df):
    # Drop full row duplicates
    df = df.drop_duplicates(df.columns, keep='first')
    df_len = len(df.index)
    # Reset the ID field for rows that have duplicate IDs, but not fully duplicated data
    df.loc[df['ID'].duplicated(), :]['ID'].apply(lambda x:  int(x)+df_len)
    return df

# Checks to see if all columns in the header have unique names.  If they don't, add an int value to the header name(s) that are duplicate
def check_header(header):
    header_set = []
    c = 0
    for i in range(len(header)):
        if header[i] in header_set:
            while header[i] + c in header_set:
                c = c + 1
            header_set.append(header[i]+c)
            c = 0
        else:
            header_set.append(header[i])
    return header_set


def main():
    csv_file = sys.argv[1]
    read_csv(csv_file)

if __name__ == "__main__":
    main()
