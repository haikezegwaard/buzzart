from fabric.context_managers import cd
from fabric.utils import abort
import os.path
import tempfile

from fabric.api import env, task, require, local

from utils import TmpDirectory


@task
def pack(branch=None, out_file_path=None):
    '''Pack a repository into a .tar.bz2'''
    require('project_name')
    require('repository')
    tmp_prefix = '{}-'.format(env.project_name)

    if hasattr(env, 'git_branch'):
        branch = env.git_branch

    if not branch:
        abort('no git branch specified, please specify one in the config.py environment. aborting ...')

    if not out_file_path:
        handle, out_file_path = tempfile.mkstemp(prefix=tmp_prefix,
                                                 suffix='.tar.bz2')
    tar(branch, out_file_path)
    env.packed_file = out_file_path


def tar(branch, out_file_path):
    if not branch:
        raise ValueError('missing required branch argument')
    if not out_file_path:
        raise ValueError('missing required out_file path')
    local('cd {0} && pwd'.format(env.project_root))
    local('cd {0} && git archive {1} | bzip2 > {2}'.format(env.project_root, branch, out_file_path))

