from charmhelpers.core import host
from cloudfoundry import contexts
from path import path
import yaml
from subprocess import call
import utils
from utils import shell
from utils import home


def setup_uaac_client(service_name):
    uaactx = contexts.UAARelation()
    orchctx = contexts.OrchestratorContext()
    secretctx = contexts.StoredContext(utils.secrets_file, {
        'ui_secret': host.pwgen(20),
    })
    domain = orchctx[orchctx.name][0]['domain']
    uaa_secret = uaactx[uaactx.name][0]['admin_client_secret']
    ui_secret = secretctx['ui_secret']

    shell("uaac target http://uaa.%s" % domain)
    shell("uaac token client get -s %s" % uaa_secret)
    client_needs_setup = bool(call(". %s/.boilerplate && uaac client get admin_ui_client" % home))
    if client_needs_setup:
        authorities = yaml.safe_load(shell('uaac client get admin'))['authorities']
        if 'scim.write' not in authorities:
            authorities += ' scim.write'
            shell('uaac client update admin --authorities "%s"' % authorities)
            shell('uaac token client get admin -s admin-secret')
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
    orchctx = contexts.OrchestratorContext()
    dbctx = contexts.MysqlRelation()
    ccdbctx = contexts.CloudControllerDBRelation()
    natsctx = contexts.NatsRelation()
    uaadbctx = None  # XXX
    template = yaml.safe_load(source.text())

    domain = orchctx[orchctx.name][0]['domain']
    ui_secret = secretctx['ui_secret']
    ccdb_uri = ccdbctx[ccdbctx.name][0]['dsn']  # ccdbctx.get('dsn', unit=0) would be nice
    db_uri = dbctx[dbctx.name][0]['dsn']
    nats_uri = 'nats://{user}:{password}@{address}:{port}'.format(**natsctx[natsctx.name][0])
    uaadb_uri = ''  # XXX

    template['uaa_client']['secret'] = ui_secret
    template['cloud_controller_uri'] = 'http://api.%s' % domain
    template['ccdb_uri'] = ccdb_uri
    template['db_uri'] = db_uri
    template['uaadb_uri'] = uaadb_uri
    template['mbus'] = nats_uri

    dest.write_text(yaml.safe_dump(template))
