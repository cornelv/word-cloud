#!/bin/bash

sudo apt-get install mysql-server libffi-dev libssl-dev libmysqlclient-dev
virtualenv ../virtenv
source ../virtenv/bin/activate && pip install -r requerments.txt
