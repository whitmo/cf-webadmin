#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions


def manage():
    manager = ServiceManager([
        {
            'service': 'cf-webadmin',
            'ports': [],  # ports to after start
            'provided_data': [
                helpers.HttpRelation()
            ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
            ],
            'data_ready': [
                actions.render_webadmin_config,
                helpers.render_template(
                    source='upstart.conf',
                    target='/etc/init.d/cf-webadmin'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
