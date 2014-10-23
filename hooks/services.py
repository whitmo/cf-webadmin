#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
from cloudfoundry.contexts import MysqlRelation
from cloudfoundry.contexts import NatsRelation
from cloudfoundry.contexts import UAARelation
from cloudfoundry.contexts import CloudControllerRelation
from cloudfoundry.contexts import CloudControllerDBRelation

import actions


def manage():
    manager = ServiceManager([
        {
            'service': 'cf-webadmin',
            'ports': [],  # ports to after start
            'provided_data': [
                #helpers.HttpRelation()
            ],
            'required_data': [
                MysqlRelation(),
                NatsRelation(),
                UAARelation(),
                CloudControllerDBRelation(),
                # UAADBRelation(),
            ],
            'data_ready': [
                actions.setup_uaac_client,
                actions.render_webadmin_config,
                helpers.render_template(
                    source='upstart.conf',
                    target='/etc/init/cf-webadmin.conf'),
            ],
        },
    ])
    manager.manage()
