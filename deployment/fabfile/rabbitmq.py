"""Fabric tasks to configure and monitor a rabbitmq server instance."""
from fabric.api import task, sudo


def _rabbitmqctl(command, *args):
    sudo('rabbitmqctl {} {}'.format(command, 
                                    ' '.join('"{}"'.format(arg) for arg in args)))


@task
def list_users():
    _rabbitmqctl('list_users')


@task
def add_user(username, password):
    _rabbitmqctl('add_user', username, password)


@task
def delete_user(username):
    _rabbitmqctl('delete_user', username)


@task
def add_vhost(vhost_path):
    _rabbitmqctl('add_vhost', vhost_path)


@task
def delete_vhost(vhost_path):
    _rabbitmqctl('delete_vhost', vhost_path)


@task
def set_permissions(vhost_path, user, conf='.*', write='.*', read='.*'):
    _rabbitmqctl('set_permissions -p {}'.format(vhost_path),
                 user, conf, write, read)


@task
def status():
    _rabbitmqctl('status')

@task
def set_policy(vhost_path, name, pattern, definition, apply_to=None):
    cmd = 'set_policy -p {}'.format(vhost_path)
    if apply_to:
        cmd += ' --apply-to {}'.format(apply_to)
    cmd += ' {} {} {}'.format(name, pattern, definition)
    _rabbitmqctl(cmd)

