from fabric.api import env, prefix, task, require, cd, sudo


def context(virtualenv_dir):
    '''Context manager for running `inside` a virtualenv (for remote commands)'''
    return prefix('. {}bin/activate'.format(virtualenv_dir))


@task
def create(virtualenv_dir=None, exec_cmd=sudo):
    '''Create a new virtualenv'''
    if virtualenv_dir is None:
        require('virtualenv_dir')
        virtualenv_dir = env.virtualenv_dir
    exec_cmd('virtualenv --no-site-packages {}'.format(virtualenv_dir))


@task(alias='remove')
def delete(virtualenv_dir=None, exec_cmd=sudo):
    ''' Delete an existing virualenv'''
    if virtualenv_dir is None:
        require('virtualenv_dir')
        virtualenv_dir = env.virtualenv_dir
    exec_cmd('rm -rf {}'.format(virtualenv_dir))
