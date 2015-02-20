import os.path
import urlparse
import tempfile

from fabric.api import env, task, require, local

from utils import TmpDirectory


@task
def pack(path=None, out_filepath=None):
    '''Pack a repository into a .tar.bz2'''
    require('project_name')
    require('repository')
    tmp_prefix = '{}-'.format(env.project_name)

    if path is None:
        path = 'trunk/'
    if hasattr(env, 'svn_branch'):
        path = env.svn_branch

    if not out_filepath:
        handle, out_filepath = tempfile.mkstemp(prefix=tmp_prefix,
                                                suffix='.tar.bz2')
    with TmpDirectory(prefix=tmp_prefix) as tmp_path:
        # TODO: validate repository and path
        assert env.repository.url.endswith('/')
        assert not path.startswith('/')
        svn_path = '{}{}'.format(env.repository.url, path)
        output_dir = os.path.join(tmp_path, 'export')
        export(svn_path, output_dir)
        tar(output_dir, out_filepath)
    env.packed_file = out_filepath


def tar(directory, out_filepath):
    if not directory:
        raise ValueError('missing required directory argument')
    if not os.path.exists(directory):
        raise ValueError('directory {} does not exist'.format(directory))
    if not out_filepath:
        raise ValueError('missing required out_filepath')
    local('tar --create --auto-compress'
          ' --directory {dir} --file {out} .'.format(
        dir=directory, out=out_filepath))


def export(svn_url, output_dir):
    local('svn export -q {repo} {output_dir}'.format(
        repo=svn_url,
        output_dir=output_dir))

