from fabric.api import task, env, run, local


@task
def copy_key():
    """ Copy your public key to remote's authorized_keys """
    local('ssh-copy-id %s' % env.host_string)
