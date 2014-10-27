#!/bin/bash

cd /opt/admin-ui
#. ~ubuntu/.boilerplate
export PATH=$PATH:/home/ubuntu/.rbenv/shims
bin/admin -c /etc/cf-webadmin.yml
