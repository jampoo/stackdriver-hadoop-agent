import jinja2
import os.path
import sys
import subprocess
import argparse

hadoop_template = 'hadoop-custom-metrics.conf.jinja'


def read_metric_list_from_textfile(text_file):
    service_dict = {}
    attribute_list = []
    for line in text_file.readlines():
        # TODO(zhanbo): verify the format
        service_attribute = line.split('.')
        service = service_attribute[0].strip()
        if not(service_dict.has_key(service)) :
            service_dict[service] = '1'  # put dumb value
        attribute_list.append(line.strip())
    return (service_dict.keys(), attribute_list)

def create_stackdriver_plugin(service_list, attribute_list, templates_dir):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=['jinja2.ext.do'])

    print env.get_template(hadoop_template).render(service_list = service_list, attribute_list = attribute_list)
    

def main():
    parser = argparse.ArgumentParser(
        description='Setup the Stackdriver agent to collect Hadoop metrics.')
    parser.add_argument('-w', '--whitelist', type=file)
    parser.add_argument('-d', '--templates_dir', type=str, \
        default='/usr/local/share/google/dataproc/jinja/templates/')
    args = parser.parse_args()
    if args.whitelist is not None:
        result = read_metric_list_from_textfile(args.whitelist)
        print result
        create_stackdriver_plugin(result[0], result[1], args.templates_dir)

if __name__ == "__main__":
    main()
