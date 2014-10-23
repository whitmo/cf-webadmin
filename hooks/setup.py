import subprocess


def pre_install():
    """
    Do any setup required before the install hook.
    """
    install_charmhelpers()

    from charmhelpers import fetch
    fetch.apt_install(fetch.filter_installed_packages(['bzr']))

    cflib = 'bzr+http://bazaar.launchpad.net/~cf-charmers/charms/trusty/cloudfoundry/trunk#egg=cloudfoundry'
    subprocess.check_call(['pip', 'install', '-e', cflib])
    subprocess.check_call(['pip', 'install', 'path.py'])


def install_charmhelpers():
    """
    Install the charmhelpers library, if not present.
    """
    try:
        import charmhelpers  # noqa
    except ImportError:
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip'])
        subprocess.check_call(['pip', 'install', 'charmhelpers'])
