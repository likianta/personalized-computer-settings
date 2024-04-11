import os
import sys

from lk_utils import call_once
from lk_utils import fs
from lk_utils import mklink
from lk_utils import timestamp


@call_once()
def _change_dir_to_likianta_home() -> None:
    # noinspection PyCompatibility
    match sys.platform:
        case 'linux':
            os.chdir('/home/likianta/Desktop')
        case 'win32':
            os.chdir('D:/Likianta')  # TEST


def main() -> None:
    # root = 'shortcut'
    
    # noinspection PyCompatibility
    match sys.platform:
        # case 'linux':
        #     io_map = {
        #         'temp/{date}': '...',
        #     }
        case 'win32':
            io_map = {
                'apps'                                  : '...',
                'apps/nushell/{ver}/nu.exe'             : 'shortcut/nushell.exe',
                'apps/python/3.12'                      : 'shortcut/python-3.12',
                'documents'                             : '...',
                'documents/appdata'                     : '...',
                'documents/gitbook-ssg'                 : 'shortcut/gitbook',
                'temp'                                  : '...',
                'temp/{date}'                           : '...',
                'workspace'                             : '...',
                'workspace/com.jlsemi.likianta'         : '...',
                'workspace/dev.master.likianta'         : '...',
                'workspace/playground/python-playground': '...',
            }
        case _:
            raise NotImplementedError
    
    for i, o in io_map.items():
        if '{ver}' in i:
            x = _find_latest_version(i.split('{ver}')[0])
            i = i.replace('{ver}', x)
        if '{date}' in i:
            x = _find_latest_version(i.split('{date}')[0])
            i = i.replace('{date}', x)
        
        if o == '...':
            o = 'shortcut/{}'.format(i.rsplit('/', 1)[-1])
        else:
            assert o.startswith('shortcut/')
        # postfix `o`
        if i.startswith('temp/'):
            yyyy_mm = timestamp('y-m')
            assert i == 'temp/{}'.format(yyyy_mm)
            assert o == 'shortcut/{}'.format(yyyy_mm)
            o = f'shortcut/temp-({yyyy_mm})'
        
        print('[red]{}[/] -> [green]{}[/]'.format(i, o), ':ir')
        mklink(i, o)


def _find_latest_date(dir: str) -> str:
    return fs.find_dir_names(dir)[-1]  # TODO


def _find_latest_version(dir: str) -> str:
    return fs.find_dir_names(dir)[-1]  # TODO


if __name__ == '__main__':
    # pox mypc_settings/make_shortcut.py
    main()
