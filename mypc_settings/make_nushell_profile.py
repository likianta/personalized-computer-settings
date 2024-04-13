import re
import sys

from argsense import cli
from lk_utils import dumps
from lk_utils import fs
from lk_utils.textwrap import join


@cli.cmd()
def main(
    file: str = None,
    pyversion: str = '3.12',  # suggest '3.11' or later
) -> None:
    # iswin = os.name == 'nt'
    # home = 'C:/Likianta' if iswin else '/Users/Likianta/Desktop'
    platform = sys.platform  # 'darwin', 'linux', 'win32'
    assert platform in ('darwin', 'linux', 'win32')
    home = (
        '/Users/Likianta/Desktop' if platform == 'darwin' else
        '/home/likianta/Desktop' if platform == 'linux' else
        'C:/Likianta'  # win32
    )
    
    match platform:
        case 'darwin':
            paths = (
                home + '/programs/alist',
                home + '/programs/bore',
                home + '/programs/caddy',
                home + '/programs/code-server/bin',
                home + '/programs/flutter/3.7/bin',
                home + '/programs/nim/2.0/bin',
                home + '/programs/nodejs/20.2/bin',
                home + '/programs/nodejs/pnpm',
                home + '/programs/nushell',
                home + '/programs/python/{}/bin'.format(pyversion),
                home + '/programs/python/pypy/3.9/bin',
                home + '/programs/rye',
                '/Users/Likianta/.bun/bin',
                '/Users/Likianta/.cargo/bin',
                '/usr/local/bin',
                '/usr/local/sbin',
                '/usr/bin',
                '/usr/sbin',
                '/bin',
            )
            env = {
                'PNPM_HOME' : home + '/programs/nodejs/pnpm',
                'PYTHONPATH': '.:lib',
            }
            alias = {
                'pip'   : 'python{} -m pip'.format(pyversion),
                'pn'    : 'pnpm',
                'pnx'   : 'pnpm run',
                'po'    : 'poetry',
                'por'   : 'poetry run',
                'pox'   : 'poetry run python',
                'py'    : 'python{}'.format(pyversion),
                'st'    : 'poetry run streamlit',
                'st_run': 'poetry run streamlit '
                          '--server.headless true --server.port',
            }
        case 'linux':
            paths = (
                home + '/programs/alist',
                home + '/programs/bore',
                home + '/programs/nim/2.0/bin',
                home + '/programs/nodejs/20.2/bin',
                home + '/programs/nodejs/pnpm',
                home + '/programs/nushell',
                home + '/programs/python/{}/bin'.format(pyversion),
                home + '/programs/rye',
                '/usr/local/bin',
                '/usr/local/sbin',
                '/usr/bin',
                '/usr/sbin',
                '/bin',
            )
            env = {
                'PNPM_HOME' : home + '/programs/nodejs/pnpm',
                'PYTHONPATH': '.:lib',
            }
            alias = {
                'pip'   : 'python{} -m pip'.format(pyversion),
                'pn'    : 'pnpm',
                'pnx'   : 'pnpm run',
                'po'    : 'poetry',
                'por'   : 'poetry run',
                'pox'   : 'poetry run python',
                'py'    : 'python{}'.format(pyversion),
                'st'    : 'poetry run streamlit',
                'st_run': 'poetry run streamlit '
                          '--server.headless true --server.port',
            }
        case 'win32':
            paths = (
                home + '/apps/bore',
                home + '/apps/caddy',
                home + '/apps/flutter/3.7/bin',
                home + '/apps/git/bin',
                home + '/apps/go/1.20/bin',
                home + '/apps/nim/2.0/bin',
                home + '/apps/nodejs/20.3/bin',
                home + '/apps/nodejs/global_modules',
                home + '/apps/nodejs/pnpm',
                home + '/apps/nushell',
                home + '/apps/python/{}'.format(pyversion),
                home + '/apps/python/{}/Scripts'.format(pyversion),
                home + '/apps/rye',
                home + '/apps/vscode/bin',
                'C:/Windows',
                'C:/Windows/System32',
                'C:/Windows/System32/OpenSSH',
                'C:/Windows/System32/Wbem',
            )
            env = {
                'NODE_PATH' : home + '/apps/nodejs/global_modules/node_modules',
                'PNPM_HOME' : home + '/apps/nodejs/pnpm',
                'PYTHONPATH': '".;lib"',
            }
            alias = {
                'pip'   : 'python -m pip',
                'pn'    : 'pnpm.exe',
                'pnx'   : 'pnpm.exe run',
                'po'    : 'poetry',
                'por'   : 'poetry run',
                'pox'   : 'poetry run python',
                'py'    : 'python',
                'st'    : 'poetry run streamlit',
                'st_run': 'poetry run streamlit '
                          '--server.headless true --server.port',
            }
        case _:
            raise Exception
    # paths = (x for x in paths if fs.exists(x))
    
    output = [
        '# this file is auto generated/updated by {}'.format(
            '[make_nushell_profile.py](https://github.com/likianta/personal'
            '-settings/blob/main/mypc_settings/make_nushell_profile.py)'
        ),
        '$env.PROMPT_COMMAND = {{|| $env.PWD | split row "{}" | last }}'
        .format('/' if platform != 'win32' else '\\\\'),
        '$env.LIKIANTA_HOME = "{}"'.format(home),
        '',
        '$env.PATH = [\n    {}\n]'.format(join((f'"{x}",' for x in paths), 4)),
        '',
        *('$env.{} = {}'.format(k, v) for k, v in env.items()),
        '',
        *('alias {} = {}'.format(k, v) for k, v in alias.items()),
    ]
    
    file = file or home + '/documents/appdata/nushell/likianta-profile.nu'
    dumps(output, file, 'plain')
    print(f'file is saved to "{file}"')


def _pick_latest_version(dir: str) -> str:
    ver_pattern = re.compile(r'[.0-9]+')
    vers = []
    for d in fs.find_dirs(dir):
        if m := ver_pattern.fullmatch(d.name):
            vers.append(m.group())
    match len(vers):
        case 0:
            raise Exception(
                'no subfolder contains version info under this dir', dir
            )
        case 1:
            return vers[0]
        case _:
            vers.sort(key=lambda x: tuple(map(int, x.split('.'))))
            return vers[-1]


if __name__ == '__main__':
    # pox mypc_settings/make_nushell_profile.py
    # pox mypc_settings/make_nushell_profile.py <custom_file>
    cli.run(main)
