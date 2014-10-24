#!/bin/bash

cd /opt/admin-ui
. ~ubuntu/.boilerplate
bundle exec bin/admin -c /etc/cf-webadmin.yml
