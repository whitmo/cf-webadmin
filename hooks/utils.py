from charmhelpers.core.hookenv import log
import subprocess
from path import path


home = path('/home/ubuntu')
secrets_file = path('/etc/admin_ui_secrets')


def shell(cmd, boilerplate=". %s/.boilerplate &&" % home):
    cmd = "%s %s" % (boilerplate, cmd)
    log(cmd)
    return subprocess.check_output(cmd, shell=True)
