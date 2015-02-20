from fabric.api import task, require, env, run
from fabfile.utils import shell_escape  # @UnresolvedImport


@task
def backup(db_config=None, exec_cmd=run, outfile='None'):
    if db_config is None:
        require('database')
        db_config = env.database
    if not outfile:
        outfile = '{}-dump.sql.bz2'.format(db_config.name)

    exec_cmd('mysqldump'
             ' --user={user}'
             ' --password={password}'
             ' --host={host}'
             ' --port={port}'
             ' {db_name}'
             ' | bzip2 --best '
             ' > {outfile}'.format(
        db_name=shell_escape(db_config.name),
        user=shell_escape(db_config.user),
        password=shell_escape(db_config.password),
        host=db_config.host,
        port=db_config.port,
        outfile=outfile
    )
    )
    env.database_backup_remote_file = outfile


@task
def create(exec_cmd=run):
    require('database')
    db = env.database

    exec_cmd('echo "CREATE DATABASE \`{db_name}\` CHARACTER SET utf8;"'
             '|mysql --batch'
             ' --user={user}'
             ' --password={password}'
             ' --host={host}'
             ' --port={port}'
             ' --default-character-set=utf8'.format(
        db_name=shell_escape(db.name),
        user=shell_escape(db.user),
        password=shell_escape(db.password),
        host=db.host,
        port=db.port,
    ),
             shell=False
    )
    """
    exec_cmd('mysqladmin'
          ' --user={user}'
          ' --password={password}'
          ' --host={host}'
          ' --port={port}'
          ' --default-character-set=utf8'
          ' create {db_name}'.format(
                      db_name=shell_escape(db.name),
                      user=shell_escape(db.user),
                      password=shell_escape(db.password),
                      host=db.host,
                      port=db.port,
                      )
    )
    """
