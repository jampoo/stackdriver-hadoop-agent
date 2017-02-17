#!/usr/bin/python
"""
Renders a template to a collectd config.


Copyright 2015 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import jinja2
import os.path
import sys
import csv

hadoop_conf_jinja_file = './hadoop-custom-metrics.conf.jinja'
hadoop_metric_whitelist = './hadoop-metric-whitelist.csv'

hadoop_metrics_upload_list = []

with open(hadoop_metric_whitelist, 'rb') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if row['upload'] == 'TRUE':
            metric_name_concat = '-'.join([row['context'], row['service'], row['name']])
            hadoop_metrics_upload_list.append(metric_name_concat)

#print hadoop_metrics_upload_list

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(sys.argv[0]) or "."),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=['jinja2.ext.do'])

print env.get_template(hadoop_conf_jinja_file).render(upload_list = hadoop_metrics_upload_list)

