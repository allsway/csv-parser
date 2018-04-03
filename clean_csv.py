#!/usr/bin/env python

import sys
import csv
import re

def read_csv(file):
    f = open(file,'rt')
    try:
        reader = csv.reader(f)
        header = next(reader)
        new_row = []
        for row in reader:
            # throw out blank rows
            if len(row) > 0:
                concat = ','.join(row[1:])
                if row[0].isdigit():
                    id = row[0]
                    p = re.compile(r'\d{5}')
                    #address = p.findall(concat)
                    zip_match = re.search(p,concat)
                    address = ''
                    zipcode = ''
                    if zip_match:
                        address = clean_address(concat[0:zip_match.start()])
                        zipcode = concat[zip_match.start():zip_match.end()]
                        website = concat[zip_match.end():]
                    # If the zipcode isn't fully there, do another type of search
                    # look for 5 numbers prior to 'www'
                    print(id,address,zipcode,website)

    finally:
        f.close()


def clean_address(address):
    address = address.replace('"','')
    address  = address.replace('\r\n',',')
    return address

def reduce_zip(zip):
    zip = re.sub('[^0-9]','',zip)
    return zip[:5]

csv_file = sys.argv[1]
read_csv(csv_file)
