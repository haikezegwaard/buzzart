import tempfile
import shutil
import re


class TmpDirectory(object):
    '''ContextManager for using a temporary directory, which is deleted after use.
        contructor params map to tempfile.mkdtemp
    '''

    def __init__(self, suffix='', prefix=tempfile.gettempprefix(), dir=None):
        self.path = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)

    def __enter__(self):
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.path)


class AttrDict(dict):
    '''dictionary making they key als available as attributes'''

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


# escape shell command parameters
# python 2.x has this hidden inside pipes module
# but let's just already use the 3.3 impl.


try: #python 3.3
    import shlex.quote as shell_escape
except ImportError:
    _find_unsafe = re.compile(r'[^\w@%+=:,./-]').search

    def _shlex_quote(s):
        """Return a shell-escaped version of the string *s*."""
        if not s:
            return "''"
        if _find_unsafe(s) is None:
            return s

        # use single quotes, and put single quotes into double quotes
        # the string $'b is then quoted as '$'"'"'b'
        return "'" + s.replace("'", "'\"'\"'") + "'"

    shell_escape = _shlex_quote
