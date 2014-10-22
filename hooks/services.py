#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions

def install_boilerplate(*args):
    pass


def manage():
    manager = ServiceManager([
        {
            'service': 'cf-admin-ui',
            'ports': [],  # ports to after start
            'provided_data': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
            ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
            ],
            'data_ready': [
                install_boilerplate,
                helpers.render_template(
                    source='upstart.conf',
                    target='/etc/init.d/cf-admin-ui'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
