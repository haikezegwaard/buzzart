from fabric.api import *



def production():
    env.user = 'hz'
    #env.git_user = 'trnguyen'
    env.project_path = '/home/hz/'
    env.venv_path = '/opt/virtualenvs/'
    env.project_name = 'buzzart'
    env.logs_path = '/home/hz/logs/'
    env.hosts = ['django-dev.fam']
    env.repo = 'svn://svn.fam/data/svn/buzzart'

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

def copy_nginx_config():
    run('cp %(project_path)s/%(project_name)s/configs/nginx/default /etc/nginx/sites-available/' % env)


def copy_supervisor_config():
    run('cp %(project_path)s/%(project_name)s/configs/supervisor/guni.conf /etc/supervisor/conf.d/' % env)


def copy_config_files():
    copy_nginx_config()
    copy_supervisor_config()


def restart_server():
    run('service nginx restart')
    run('supervisorctl restart gunicorn')