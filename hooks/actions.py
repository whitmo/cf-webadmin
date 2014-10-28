from charmhelpers.core import host
from cloudfoundry import contexts
from functools import partial
from path import path
from subprocess import call
from utils import home
from utils import shell
import utils
import yaml


uaac_path = 'export PATH="/opt/uaac/bin:$PATH"'
shell = partial(shell, boilerplate=uaac_path)


def setup_uaac_client(service_name):
    uaactx = contexts.UAARelation()
    orchctx = contexts.OrchestratorRelation()
    secretctx = contexts.StoredContext(utils.secrets_file, {
        'ui_secret': host.pwgen(20),
    })
    domain = orchctx[orchctx.name][0]['domain']
    uaa_secret = uaactx[uaactx.name][0]['admin_client_secret']
    ui_secret = secretctx['ui_secret']

    shell("uaac target http://uaa.%s" % domain)
    shell("uaac token client get admin -s %s" % uaa_secret)
    client_needs_setup = bool(call("%s && uaac client get admin_ui_client" % uaacc_path, shell=True))
    if client_needs_setup:
        authorities = yaml.safe_load(shell('uaac client get admin'))['authorities']
        if 'scim.write' not in authorities:
            authorities += ' scim.write'
            shell('uaac client update admin --authorities "%s"' % authorities)
            shell("uaac token client get admin -s %s" % uaa_secret)
        shell('uaac group add admin_ui.admin')
        shell('uaac member add admin_ui.admin admin')
        shell('uaac client add admin_ui_client'
              ' --authorities cloud_controller.admin,cloud_controller.read,cloud_controller.write,openid,scim.read'
              ' --authorized_grant_types authorization_code,client_credentials,refresh_token'
              ' --autoapprove true'
              ' --scope admin_ui.admin,admin_ui.user,openid'
              ' -s %s' % ui_secret)


def render_webadmin_config(service_name,
                           source=path("/opt/admin-ui/config/default.yml"),
                           dest=path('/etc/cf-webadmin.yml')):
    secretctx = contexts.StoredContext(utils.secrets_file, {})
    orchctx = contexts.OrchestratorRelation()
    ccdbctx = contexts.CloudControllerDBRelation()
    dbctx = contexts.MysqlRelation()
    uaadbctx = contexts.UAADBRelation()
    natsctx = contexts.NatsRelation()
    template = yaml.safe_load(source.text())

    ui_secret = secretctx['ui_secret']
    domain = orchctx.get_first('domain')
    ccdb_uri = ccdbctx.get_first('dsn')
    db_uri = dbctx.get_first('dsn')
    uaadb_uri = uaadbctx.get_first('dsn')
    nats_uri = 'nats://{user}:{password}@{address}:{port}'.format(**natsctx[natsctx.name][0])

    template['uaa_client']['secret'] = ui_secret
    template['cloud_controller_uri'] = 'http://api.%s' % domain
    template['ccdb_uri'] = ccdb_uri
    template['db_uri'] = db_uri
    template['uaadb_uri'] = uaadb_uri
    template['mbus'] = nats_uri

    dest.write_text(yaml.safe_dump(template))
