"""Linux specific tasks."""
from fabric.api import task, run, settings, hide
from fabric import colors

@task
def host_type():
    """ Output the type of remote host"""
    output = run('uname -s')
    if output == 'Linux':
        print(colors.green(output, bold=True))
    else:
        print(colors.red(output, bold=True))

@task
def host_name():
    """Output hostname."""
    output = run('hostname')
    print(colors.green(output, bold=True))

@task
def host_ip():
    """Output IP address (of the hostname)"""
    output = run('hostname -i')
    print(colors.green(output, bold=True))


@task
def release_info():
    with settings(hide('everything')):
        lsb_release = run('lsb_release -a', warn_only=True, quiet=True)
        if lsb_release.succeeded:
            print(colors.green(lsb_release, bold=True))
        else:
            output = run('cat /etc/lsb-release')
            print(colors.green(output, bold=True))
