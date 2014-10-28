from charmhelpers.core.hookenv import log
import subprocess
from path import path
import os

home = path('/home/ubuntu')
secrets_file = path('/etc/admin_ui_secrets')


def shell(cmd, prefix="", env=None):
    environ = dict(os.environ)
    if not env is None:
        environ.update(env)

    cmd = " ".join([x for x in (prefix, cmd) if x])
    log(cmd)

    try:
        return subprocess.check_output(cmd, shell=True, env=environ)
    except subprocess.CalledProcessError as e:
        log("FAILED %s: %s" % (cmd, e.output))
        raise
