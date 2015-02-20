""" Configuration(s) for the project and different hosts
"""
from fabric.operations import local
import os
from os.path import realpath, normpath, dirname, join, expanduser, expandvars
from fabric.api import env, task, require, abort

from .django import get_settings as get_django_settings
from .utils import AttrDict

env.use_ssh_config = True # try and use some settings from $HOME/.ssh/config

env.project_name = 'buzzart'
env.project_root = normpath(join(dirname(__file__), '..', '..'))
env.project_django_root = env.project_root

env.repository = AttrDict(
    type='git',
    url='git@bitbucket.org:fundamentallmedia/buzzart.git'
)

env.django_project = ''  # default django project (dir)

env.django_manage_commands = ('syncdb --noinput',
                              'migrate',
                              'collectstatic --noinput'
                              )

env.ubuntu_base_packages = [ # dep. for all installations
    # Base python env (need gcc to compile python modules)
    'gcc', 'g++', 'python-dev', 'python-virtualenv',
    # req. for certain python packages (which will be installed in virtualenv)
    'libmysqld-dev', 'gettext', 'libcurl4-openssl-dev',
    'zlib1g-dev', 'libjpeg62-dev', 'libfreetype6-dev',
    'librtmp-dev', 'libgnutls-dev',
    'mercurial', 'git'
]

env.ubuntu_required_packages = env.ubuntu_base_packages + [ # dep.for 'web' app
    # apache, this should pull in the rest of apache2
    'libapache2-mod-wsgi',
]

env.rabbitmq = AttrDict(username='buzzart',
                        password='buzzart',
                        vhost='buzzart')

env.deploy_docs = False
env.additional_databases = None
env.using_apache = True
env.using_supervisor = False
env.git_branch = local('git rev-parse --abbrev-ref HEAD',capture=True)

print '##################################################################'
print 'branch = {0}'.format(env.git_branch)
print '##################################################################'

def test():
    pass


@task(alias='acc')
def acceptation():
    '''Configuration for acceptation server'''
    env.project_name = 'buzzart-acc'
    env.hosts = ['django-dev.fundament.nl']
    env.install_dir = '/opt/buzzart/'
    env.install_user = 'hz'
    env.django_media_root = '/opt/buzzart/media/'
    env.requirements_file = join(env.project_root,
                                 'requirements.txt')
    env.virtualenv_dir = '/opt/virtualenvs/buzzart/'
    env.django_settings = 'settings.acceptation'
    django_settings_to_env()
    env.django_developing = False


@task(aliases=('prod', 'live'))
def production():
    '''Configuration for production server'''
    env.project_name = 'buzzart'
    env.hosts = ['django01.fun.famhosting.nl']
    env.install_dir = '/opt/buzzart/'
    env.install_user = 'buzzart'
    env.django_media_root = '/opt/buzzart/media/'
    env.requirements_file = join(env.project_root,
                                 'requirements.txt')
    env.virtualenv_dir = '/opt/virtualenvs/buzzart/'
    env.django_settings = 'settings.production'
    django_settings_to_env()
    env.django_developing = False

def django_settings_to_env():
    '''Export some settings from Django to Fabric's env'''
    require('django_settings')
    settings = get_django_settings()
    db_settings = settings.DATABASES['default']
    env.database = _django_dbsettings_to_dict(db_settings)
    for extra_dbs in [db for db in settings.DATABASES if db is not 'default']:
        extra_db_settings = settings.DATABASES[extra_dbs]
        dbconf = _django_dbsettings_to_dict(extra_db_settings)
        if not env.additional_databases:
            env.additional_databases = []
        env.additional_databases.append(dbconf)


def _django_dbsettings_to_dict(db_settings):
    db_engine = db_settings['ENGINE']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_host = db_settings['HOST']
    db_port = db_settings['PORT']
    return AttrDict(
        type=_django_engine_to_type(db_engine),
        host=db_host,
        port=db_port,
        name=db_name,
        user=db_user,
        password=db_password
    )


def _django_engine_to_type(engine):
    if 'mysql' in engine:
        return 'mysql'
    elif 'sqlite' in engine:
        return 'sqlite'
    elif 'postgres' in engine:
        return 'postgres'
    else:
        abort("Unknown Django database engine '{}'".format(engine))
