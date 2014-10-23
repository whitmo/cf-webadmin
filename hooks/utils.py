from charmhelpers.core.hookenv import log
import subprocess

home = path('/home/ubuntu')


def shell(cmd, boilerplate=". %s/.boilerplate &&" % home):
    cmd = "%s %s" % (boilerplate, cmd)
    log(cmd)
    return subprocess.check_call(cmd, shell=True)
