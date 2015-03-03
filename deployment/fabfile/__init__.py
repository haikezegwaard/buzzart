import time
import functools
import os.path

from fabric.api import *
from fabric import colors
from fabric.contrib import files

# fabric hosts + configuration is set in:
from . import config

# relative import, prevent clashing with the 'real' libs/apps
from . import system
from . import ubuntu
from . import git
from . import svn
from . import virtualenv
from . import pip
from . import database as db
from . import django
from . import sphinx
from . import rabbitmq
# from . import amazon

from .utils import TmpDirectory

provided_by_config = (config.test, config.acceptation, config.production)


@task
def upgrade():
    '''Upgrade an existing install'''
    require('install_user')
    require('hosts')
    if not prompt('Upgrading {} with {}. Sure? CTRL-C to abort'.format(
            env.hosts, env.git_branch), default='y'):
        abort('Abort')

    # on 'new' install we can't backup
    # just create them and backup empties
    if not files.exists(env.install_dir):
        sudo('mkdir -p {dir}'.format(dir=env.install_dir))
        sudo('chown {user}.{user} {dir}'.format(user=env.install_user,
                                                dir=env.install_dir))
    if not files.exists(env.django_media_root):
        sudo('mkdir -p {dir}'.format(dir=env.django_media_root))
        sudo('chown {user}.{user} {dir}'.format(user=env.install_user,
                                                dir=env.django_media_root))

    pack()
    upload()
    backup() 

    print(colors.red('TODO: impl. upload pip requirements bundle', bold=True))

    tmp_install_dir = '{}_new/'.format(env.install_dir[:-1])  # strip '/'
    sudo('mkdir -p {}'.format(tmp_install_dir))
    sudo('chown {user}.{user} {dir}'.format(user=env.install_user,
                                            dir=tmp_install_dir))

    print(colors.red('TODO: activate a maintenance page?', bold=True))

    with cd(tmp_install_dir):
        sudo('tar -xf {}'.format(env.uploaded_packed_file),
             user=env.install_user)
        sudo('rm {}'.format(env.uploaded_packed_file))
        with virtualenv.context(env.virtualenv_dir):
            sudo_as = functools.partial(sudo, user=env.install_user)
            django.project_manage_upgrade(exec_cmd=sudo_as)

    # move/rename dirs
    install_backup_dir = '{}_old/'.format(env.install_dir[:-1])  # strip '/'
    sudo('rm -rf {install_backup_dir}'.format(
        install_backup_dir=install_backup_dir))
    sudo('mv {install_dir} {install_backup_dir} && '
         'mv {tmp_install_dir} {install_dir}'.format(
        install_dir=env.install_dir,
        install_backup_dir=install_backup_dir,
        tmp_install_dir=tmp_install_dir))

    if env.deploy_docs:
        deploy_sphinx_docs()

    if env.using_apache and not env.django_developing:
        sudo('service apache2 restart')
    if env.using_supervisor:
        sudo('supervisorctl reload')


@task
def pip_install_requirements():
    require('virtualenv_dir')
    pip.download_requirements()
    pip.upload_requirements()
    pip.install_requirements()


@task
def ubuntu_apt_get():
    require('ubuntu_required_packages')
    apt_get_params = ' '.join(env.ubuntu_required_packages)
    sudo('apt-get update')
    sudo('apt-get -q -y install {}'.format(apt_get_params))


@task
def deploy_sphinx_docs():
    """Deploy sphinx (static HTML) documentation."""
    require('docs_root', 'docs_install_dir')
    sphinx.build_html_docs(env.docs_root)
    sudo('mkdir -p {}'.format(env.docs_install_dir))
    sphinx.deploy_html_docs(env.docs_root,
                            env.docs_install_dir)

# TODO: integrate into upgrade trask
@task
def new_install():
    '''A new installation'''
    require('install_user')
    if not prompt('New installation {} with {}. Sure? CTRL-C to abort'.format(
            env.hosts, env.git_branch), default='y'):
        abort('Abort')
    pack()
    upload()

    ubuntu_apt_get()
    execute(virtualenv.create)
    pip_install_requirements()

    # TODO: check database permissions?
    db.create()

    tmp_install_dir = '{}_new/'.format(env.install_dir[:-1])  # strip '/'
    sudo('mkdir -p {}'.format(tmp_install_dir))
    sudo('chown {user}.{user} {dir}'.format(user=env.install_user,
                                            dir=tmp_install_dir))

    with cd(tmp_install_dir):
        sudo('tar -xf {}'.format(env.uploaded_packed_file),
             user=env.install_user)
        sudo('rm {}'.format(env.uploaded_packed_file))
        with cd('caire_web'), virtualenv.context(env.virtualenv_dir):
            sudo_as = functools.partial(sudo, user=env.install_user)
            django.project_manage_upgrade(exec_cmd=sudo_as)
            # TODO: loaddata categories
    sudo('mv {tmp_install_dir} {install_dir}'.format(
        tmp_install_dir=tmp_install_dir,
        install_dir=env.install_dir))
    print(colors.red('TODO: configure apache: (sym)link apache config', bold=True))


@task
def install_amq_server():
    require('rabbitmq')
    #ubuntu_apt_get()
    sudo('apt-get -q -y install rabbitmq-server')
    rabbitmq.delete_user('guest')

    rabbitmq.add_user(env.rabbitmq.username, env.rabbitmq.password)
    rabbitmq.add_vhost(env.rabbitmq.vhost)
    rabbitmq.set_permissions(env.rabbitmq.vhost, env.rabbitmq.username)
    # for 3.x
    # rabbitmq.set_policy(env.rabbitmq.vhost, 'celery-ha', '^celery$', '{"ha-mode":"all"}', apply_to='queues')


@task
def install_task_worker():
    require('install_user')
    if not prompt('New installation {} with {}. Sure? CTRL-C to abort'.format(
            env.hosts, env.git_branch), default='y'):
        abort('Abort')
    pack()
    upload()

    ubuntu_apt_get()
    virtualenv.create()
    pip_install_requirements()

    tmp_install_dir = '{}_new/'.format(env.install_dir[:-1])  # strip '/'
    sudo('mkdir -p {}'.format(tmp_install_dir))
    sudo('chown {user}.{user} {dir}'.format(user=env.install_user,
                                            dir=tmp_install_dir))

    with cd(tmp_install_dir):
        sudo('tar -xf {}'.format(env.uploaded_packed_file),
             user=env.install_user)
        sudo('rm {}'.format(env.uploaded_packed_file))
        sudo_as = functools.partial(sudo, user=env.install_user)
        django.project_manage_upgrade(exec_cmd=sudo_as)
    sudo('mv {tmp_install_dir} {install_dir}'.format(
        tmp_install_dir=tmp_install_dir,
        install_dir=env.install_dir))


@task
def backup():
    ''' Backup existing installation'''
    require('install_dir', 'install_user', provided_by=provided_by_config)
    print "backup start"
    with TmpDirectory(prefix='platform31_kks-backup') as tmp_dir:
        backup_base_dir = os.path.normpath(os.path.join(env.install_dir, '..',
                                                        'backups', env.project_name))
        backup_dir = os.path.normpath(os.path.join(backup_base_dir,
                                                   time.strftime('%Y%m%d%H%M%S')))
        sudo('mkdir -p {}'.format(backup_dir))
        with cd(backup_dir):
            db.backup(exec_cmd=sudo)
            sudo('tar -cjf {0}.tar.bz2 {1}'.format(env.project_name, env.install_dir))
            sudo('tar -cjf {0}_media.tar.bz2 {1}'.format(env.project_name, env.django_media_root))
            if env.additional_databases:
                for conf in env.additional_databases:
                    db.backup(db_config=conf, exec_cmd=sudo)
        #with lcd('/tmp/'):
            #get(backup_dir)



@task
def pack(**kwargs):
    """Pack the project into a .tar.bz2"""
    require('repository')
    #if env.repository.startswith('svn://'):
    if env.repository.type == 'svn':
        execute(svn.pack, **kwargs)
    if env.repository.type == 'git':
        execute(git.pack, **kwargs)
    else:
        abort('Unsupported repository type %s' % env.repository)


@task
def upload():
    '''Upload the packed project files to remote server'''
    require('packed_file', provided_by=pack)
    puts = put(env.packed_file, '/tmp/')
    env.uploaded_packed_file = puts[0]


