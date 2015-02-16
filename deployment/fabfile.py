from fabric.api import *
from fabric.api import task
from fabric.contrib.project import upload_project

env.user = 'hz'
#env.git_user = 'trnguyen'
env.project_path = '/opt/'
env.venv_path = '/opt/virtualenvs/'
env.project_name = 'buzzart'
env.logs_path = '/opt/log/'
env.hosts = ['django-dev.fam']
env.repo = 'svn://svn.fam/data/svn/buzzart'


@task
def test():
    local('cd c:\\tmp')
    local('svn export --force %(repo)s/trunk c:\\tmp\\buzzart' % env)
    # make sure the directory is there!
    #upload_project('c:\\tmp\\buzzart', '/tmp/buzzart')
    #put('c:\\tmp\\buzzart','/tmp/buzzart')
    zipfolder()


@serial
def zipfolder():
    local('tar czf buzzart.tgz buzzart')


def checkout_trunk():
    run('cd %(project_path)s;\
        svn co %(repo)s;' % env)

def update_trunk():
    run('cd %(project_path)s/%(project_name)s/trunk;\
        svn up %(repo)s;' % env)

def setup():
    create_all_needed_directories()
    create_virtualenv()
    #clone_repo()
    #checkout_latest()
    checkout_trunk()
    install_requirements()


def create_all_needed_directories():
    run('mkdir -p %(project_path)s;\
            mkdir -p %(venv_path)s;\
            mkdir -p %(logs_path)s' % env)


def create_virtualenv():
    run('cd %(venv_path)s; virtualenv %(project_name)s' % env)


def deploy():
    checkout_latest()
    install_requirements()
    migrate()
    create_app_super_user()
    copy_config_files()
    restart_server()


def clone_repo():
    run('cd %(project_path)s; git clone %(git_user)s@%(repo)s:/srv/repos/git/%(project_name)s' % env)


def checkout_latest():
    run('cd %(project_path)s/%(project_name)s; git pull origin master' % env)


def install_requirements():
    run('source %(venv_path)s/%(project_name)s/bin/activate;\
        cd %(project_path)s/%(project_name)s; pip install -r requirements.txt' % env)


def migrate():
    run('source %(venv_path)s/%(project_name)s/bin/activate; \
            cd %(project_path)s/%(project_name)s;\
            python manage.py syncdb --noinput --migrate' % env)


def create_app_super_user():
    run('source %(venv_path)s/%(project_name)s/bin/activate; \
            cd %(project_path)s/%(project_name)s/src/CAS;\
            python manage.py createsuperuser' % env)

def copy_apache_config():
    run('ln -s %(project_path)s/%(project_name)s/deployment/apache/buzzart-dev.conf /etc/apache2/sites-available/%(project_name)s' % env)
    run('ln -s /etc/apache2/sites-available/%(project_name)s /etc/apache2/sites-enabled/%(project_name)s' % env)


def copy_supervisor_config():
    run('cp %(project_path)s/%(project_name)s/configs/supervisor/guni.conf /etc/supervisor/conf.d/' % env)


def copy_config_files():
    copy_apache_config()
    copy_supervisor_config()


def restart_server():
    run('apachectl graceful')