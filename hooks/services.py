#!/usr/bin/python

from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers
from charmhelpers.core.services.base import ServiceManager
from cloudfoundry.contexts import CloudControllerDBRelation
from cloudfoundry.contexts import MysqlRelation
from cloudfoundry.contexts import NatsRelation
from cloudfoundry.contexts import OrchestratorRelation
from cloudfoundry.contexts import UAADBRelation
from cloudfoundry.contexts import UAARelation

import actions


def manage():
    manager = ServiceManager([
        {
            'service': 'cf-webadmin',
            'ports': [8070],  # ports to after start
            'provided_data': [
                #helpers.HttpRelation()
            ],
            'required_data': [
                OrchestratorRelation(),
                MysqlRelation(),
                NatsRelation(),
                UAARelation(),
                CloudControllerDBRelation(),
                UAADBRelation(),
                {'charm_dir': hookenv.charm_dir()},
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
