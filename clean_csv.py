#!/usr/bin/env python

import sys
import csv
import re
import pandas
import datetime

# Reads in the csv file, outputs clean csv file
def read_csv(file):

    with open(file, 'rb') as f:
        reader = csv.reader(f)
        header = next(reader)
        full_file = list(reader)

    # check for lines with the wrong number of fields first:
    full_file = remove_errors(full_file,file,header)
    # Now all fields should be of the right length, pass them to dataframe
    df = pandas.DataFrame(full_file)
    checked_column_names = check_header(header)
    df.columns = checked_column_names
    df = clean_rows(df)
    df.to_csv('corrected_' + datetime.datetime.now().strftime("%Y-%m-%d") + '_' + file,
        index=False,encoding ='utf-8')

# Gets all lines that have more fields than the header
def remove_errors(full_file,file,header):
    error_lines = []
    error_lines.append(header)
    for row in full_file:
        if len(row) > len(header):
            error_lines.append(row)
            full_file.remove(row)
        if len(row) > 0 and len(row) < len(header):
            error_lines.append(row)
            full_file.remove(row)
    if len(header) > 1:
        print(str(len(error_lines) - 1) + ' rows exist with an incorrect number of fields.  Please check the errors file')
        with open('errors_' + str(datetime.datetime.now().strftime("%Y-%m-%d")) + '_' + file, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(error_lines)
    return full_file

# For all string columns, removes bad characters
def clean_rows(df):
    df.dropna(inplace=True)
    # cleaning all string columns of newline characters, quotes, and bad characters
    for column in df:
        if df[column].dtype == 'object':
            df[column] = df[column].map(lambda x: clean_string(x))
    df = find_dupes(df)
    return df


# Removes bad characters from string fields
def clean_string(field):
    # add in any 'bad characters' as well..
    field = field.replace('"','')
    field = field.replace("'",'')
    field = field.replace('\r\n',', ')
    field = field.replace('\n',', ')
    return field

# Find and drop duplicate rows
def find_dupes(df):
    # Drop full row duplicates
    df = df.drop_duplicates(df.columns, keep='first')
    df_len = len(df.index)
    # Reset the ID field for rows that have duplicate IDs, but not fully duplicated data
    #df.loc[df['ID'].duplicated(), :]['ID'].map(lambda x:  int(x) + df_len)
    return df

# Checks to see if all columns in the header have unique names.  If they don't, add an int value to the header name(s) that are duplicate
# This is actually handled by mangle_dupe_cols...
def check_header(header):
    header_set = []
    c = 0
    for i in range(len(header)):
        if header[i] in header_set:
            while header[i] + str(c) in header_set:
                c = c + 1
            header_set.append(header[i]+'.'+str(c))
            c = 0
        else:
            header_set.append(header[i])
    return header_set


def main():
    csv_file = sys.argv[1]
    read_csv(csv_file)

if __name__ == "__main__":
    main()
