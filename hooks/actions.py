from charmhelpers.core import hookenv
from cloudfoundry import contexts
from path import path
import yaml


def log_start(service_name):
    uaacxt = contexts.UAARelation()
    hookenv.log('cf-webadmin starting')


def setup_uaac_client(name):

    pass


def render_webadmin_config(vars,
                           source=path("/opt/admin-ui/config/default.yml"),
                           dest=path('/etc/cf-webadmin.yml')):
    template = yaml.safe_load(open(source))

    dest.write_text(yaml.safe_dump(template))
