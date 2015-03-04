import tempfile
import os.path

from fabric.api import task, require, env, local, lcd, cd, put, run, sudo

from . import virtualenv
from .utils import TmpDirectory

# prevent virualenv task to be picked up as sub-task
__all__ = ['download_requirements',
           'upload_requirements',
           'install_requirements']


@task
def download_requirements():
    '''Download pip requirements.'''
    require('requirements_file')
    requirements_file = env.requirements_file
    tmp_prefix = '{}-requirements-'.format(env.project_name)
    with TmpDirectory(prefix=tmp_prefix) as tmp_dir:
        local('pip install --download {dir} -r {requirements}'.format(
            dir=tmp_dir,
            requirements=requirements_file))
        _handle, out_filepath = tempfile.mkstemp(prefix=tmp_prefix,
                                                 suffix='.tar.bz2')
        with lcd(tmp_dir):
            # include copy of requirements file
            base_requirements_file = os.path.join(env.project_root,
                                                  'requirements/base.txt')
            local('cp {} .'.format(base_requirements_file))
            local('cp {} .'.format(requirements_file))
            local('tar -cjf {file} *'.format(file=out_filepath))
        env.pip_requirements_archive = out_filepath


@task
def upload_requirements():
    '''Upload (packed) pip requirements'''
    require('pip_requirements_archive', provided_by=download_requirements)
    archive_file = env.pip_requirements_archive
    puts = put(archive_file, '/tmp/')
    env.uploaded_packed_file = puts[0]


@task
def install_requirements():
    '''Install pip requirements'''
    require('virtualenv_dir')
    require('uploaded_packed_file', provided_by=upload_requirements)
    archive = env.uploaded_packed_file
    _head, requirements_filename = os.path.split(env.requirements_file)
    tmp_dir = '/tmp/{}-requirements/'.format(env.project_name)
    run('mkdir -p {}'.format(tmp_dir))
    with cd(tmp_dir):
        run('tar -xvf {}'.format(archive))
        with virtualenv.context(env.virtualenv_dir):
            sudo('pip install --upgrade --no-index '
                 '--find-links=file://{dir} -r {requirements}'.format(
                dir=tmp_dir, requirements=requirements_filename))
        # cleanup
    run('rm -rf {}'.format(tmp_dir))
    run('rm {}'.format(env.uploaded_packed_file))
    
@task
def install_reqs():
    require('virtualenv_dir')
    require('requirements')
    with virtualenv.context(env.virtualenv_dir):
        run('pip install --upgrade -r {}'.format(env.requirements))
