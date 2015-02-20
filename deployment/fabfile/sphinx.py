"""Fabric task to deploy shinx documentation."""
import os.path

from fabric.api import env, lcd, local, put, shell_env, task


@task
def build_html_docs(root_path):
    """Build sphinx HTML documentation.

    This assumes a directory contains the common Sphinx directory structure
    with a separated source and build.
    """
    with lcd(root_path), shell_env(DJANGO_SETTINGS_MODULE=env.django_settings):
        local('make clean')
        local('make html')


@task
def deploy_html_docs(root_path, install_path):
    local_path = os.path.join(root_path, 'build/**')
    put(local_path=local_path,
        remote_path=install_path,
        use_sudo=True)
