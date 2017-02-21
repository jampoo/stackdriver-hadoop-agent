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
import subprocess
import argparse

hadoop_conf_jinja_file = './hadoop-custom-metrics.conf.jinja'
hadoop_metric_whitelist = './hadoop-metric-whitelist.csv'
stackdriver_agent_plugin_dir = '/opt/stackdriver/collectd/etc/collectd.d/'
hadoop_env_file = '/etc/hadoop/conf/hadoop-env.sh'
yarn_env_file = '/etc/hadoop/conf/yarn-env.sh'

hadoop_metrics_upload_list = []

jxm_opts_conf = """
### JMX settings
export JMX_OPTS=" -Dcom.sun.management.jmxremote.authenticate=false
    -Dcom.sun.management.jmxremote.ssl=false
    -Dcom.sun.management.jmxremote.port"
"""

hadoop_env_conf_addon = jxm_opts_conf + """
export HADOOP_NAMENODE_OPTS="$JMX_OPTS=8006 $HADOOP_NAMENODE_OPTS"
export HADOOP_SECONDARYNAMENODE_OPTS="$HADOOP_SECONDARYNAMENODE_OPTS"
export HADOOP_DATANODE_OPTS="$JMX_OPTS=8006 $HADOOP_DATANODE_OPTS"
"""
yarn_env_conf_addon = jxm_opts_conf + """
export YARN_OPTS="$JMX_OPTS=8008 $YARN_OPTS"
"""

def setup_hadoop_jmx_port() :
    with open(hadoop_env_file, 'a') as hadoop_env:
        hadoop_env.write(hadoop_env_conf_addon)
    with open(yarn_env_file, 'a') as yarn_env:
        yarn_env.write(yarn_env_conf_addon)
    print "Complete setting up jmx port on Hadoop."

def create_stackdriver_plugin() :
    with open(hadoop_metric_whitelist, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row['upload'] == 'TRUE':
    #            metric_name_concat = '-'.join([row['context'], row['service'], row['name']])
                metric_name_concat = row['name']
                hadoop_metrics_upload_list.append(metric_name_concat)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(sys.argv[0]) or "."),
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=['jinja2.ext.do'])

    # write to plugin file.
    file_plugin = open(stackdriver_agent_plugin_dir + 'hadoop.conf', 'w')
    file_plugin.write(env.get_template(hadoop_conf_jinja_file).render(upload_list = hadoop_metrics_upload_list))
    file_plugin.write('\n\n') # add empty lines in the end of plugin config.
    print "Complete creating the Stackdriver monitoring agent plugin."

def restart_daemons() :
    subprocess.Popen('service hadoop-hdfs-namenode restart')
    subprocess.Popen('service hadoop-yarn-resourcemanager restart')
    subprocess.Popen('service stackdriver-agent restart')
    print "Complete restarting all daemons."
    
def main():
    parser = argparse.ArgumentParser(description='Setup the Stackdriver agent to collect Hadoop metrics.')
    parser.add_argument('-j', '--jmx_port', action = 'store_true', default=False)
    parser.add_argument('-s', '--stackdriver_plugin', action = 'store_true', default=False)
    parser.add_argument('-d', '--daemons_restart', action = 'store_true', default=False)
    args = parser.parse_args()
    if args.jmx_port :
        setup_hadoop_jmx_port()
    if args.stackdriver_plugin :
        create_stackdriver_plugin()
    if args.daemons_restart :
        restart_daemons()

if __name__ == "__main__":
    main()

