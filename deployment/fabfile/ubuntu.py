"""Ubuntu specific task implementation."""
from fabric.api import task, sudo


@task
def install_sudo():
    apt_install('sudo')
    # TODO: configure sudo users

@task
def install_mysqld():
    apt_install('mysql-server')


def apt_install(pkg_name):
    _apt_get('update')
    _apt_get('install {}'.format(pkg_name))

def _apt_get(cmd):
    sudo('DEBIAN_FRONTEND=noninteractive apt-get -q -y {}'.format(cmd))


