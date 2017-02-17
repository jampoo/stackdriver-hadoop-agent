#!/bin/bash

apt-get -y install python-pip

pip install https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.7.2.tar.gz

python ./render_hadoop_template.py
