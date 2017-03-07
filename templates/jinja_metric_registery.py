#!/usr/bin/python

import csv
import os.path
import sys

file_path = "./jinja-metric-raw.csv"

def main() :
    with open(file_path, 'rb') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if (len(sys.argv) == 1 or row['service'] == sys.argv[1]):
                jinja_metric_name = '    ("%s", "%s"),' % (row['name'], row['value_type'])
                print jinja_metric_name

if __name__ == "__main__":
    main()

