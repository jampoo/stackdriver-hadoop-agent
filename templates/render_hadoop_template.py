import jinja2
import os.path
import sys
import subprocess
import argparse

jinja_templates_path = '/usr/local/share/google/dataproc/jinja/templates/'
hadoop_template = 'hadoop-custom-metrics.conf.jinja'

def read_metric_list_from_textfile(text_file):
    hadoop_metrics_upload_list = []
    for line in text_file.readlines():
        metric_name = line.split('.')[-1].strip()
        hadoop_metrics_upload_list.append(metric_name)
    return hadoop_metrics_upload_list

def create_stackdriver_plugin(metric_list):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(jinja_templates_path),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=['jinja2.ext.do'])

    print env.get_template(hadoop_template).render(upload_list = metric_list)

def main():
    parser = argparse.ArgumentParser(
        description='Setup the Stackdriver agent to collect Hadoop metrics.')
    parser.add_argument('-w', '--whitelist', type=file)
    args = parser.parse_args()
    if args.whitelist is not None:
        metric_list = read_metric_list_from_textfile(args.whitelist)
        create_stackdriver_plugin(metric_list)

if __name__ == "__main__":
    main()
