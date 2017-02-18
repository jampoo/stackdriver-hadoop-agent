#!/usr/bin/python

import csv
import os.path


file_path = "./jinja-metric-raw.csv"
jinja_metric_format = '("%s", "%s"),'

def main() :
    with open(file_path, 'rb') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            jinja_metric_name = jinja_metric_format % (row['value_type'], row['name'])
            print jinja_metric_name

if __name__ == "__main__":
    main()

