from charmhelpers.core import hookenv
from path import path
import yaml


def log_start(service_name):
    hookenv.log('cf-webadmin starting')


def render_webadmin_config(vars,
                           source=path("/opt/admin-ui/config/default.yml"),
                           dest=path('/etc/cf-webadmin.yml')):
    template = yaml.safe_load(open(source))

    dest.write_text(yaml.safe_dump(template))
