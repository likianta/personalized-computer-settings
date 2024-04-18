import os
import re
import sys
from textwrap import dedent

from lk_utils import call_once
from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads
from lk_utils import mklink
from lk_utils import run_cmd_args
from lk_utils import timestamp


@call_once()
def _change_dir_to_likianta_home() -> None:
    # noinspection PyCompatibility
    match sys.platform:
        case 'linux':
            os.chdir('/home/likianta/Desktop')
        case 'win32':
            os.chdir('C:/Likianta')  # TEST


def main() -> None:
    # root = 'shortcut'
    
    # noinspection PyCompatibility
    match sys.platform:
        # case 'linux':
        #     io_map = {
        #         'temp/{date}': '...',
        #     }
        case 'win32':
            io_map = loads(fs.xpath('../config/windows_shortcuts.yaml'))['map']
        case _:
            raise NotImplementedError
    
    for i, o in io_map.items():
        if '{' in i:
            a, b = i.rsplit('/', 1)
            i = a + '/' + _fill_name(b, a)
        if not fs.exists(i):
            print(':iv3', f'could not find "{i}"')
            continue
            
        if o == '...':
            o = 'shortcut/{}'.format(i.rsplit('/', 1)[-1])
        elif '{' in o:
            a, b = o.rsplit('/', 1)
            o = a + '/' + _fill_name(b)
        assert o.startswith('shortcut/')
        
        print('[red]{}[/] -> [green]{}[/]'.format(i, o), ':ir')
        if fs.exists(o):
            continue
        if sys.platform == 'win32':
            make_shortcut_win32(i, o + '.lnk')
        else:
            mklink(i, o)


def make_shortcut_win32(file_i: str, file_o: str = None) -> None:
    """
    use batch script to create shortcut, no pywin32 required.

    args:
        file_o: if not given, will create a shortcut in the same folder as -
            `file_i`, with the same base name.

    https://superuser.com/questions/455364/how-to-create-a-shortcut-using-a
    -batch-script
    https://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create
    -shortcuts/
    """
    assert os.path.exists(file_i) and not file_i.endswith('.lnk')
    if not file_o:
        file_o = fs.replace_ext(file_i, 'lnk')
    else:
        assert file_o.endswith('.lnk')
    if os.path.exists(file_o):
        os.remove(file_o)
    
    vbs = fs.xpath('../_temp.vbs')
    command = dedent('''
        Set objWS = WScript.CreateObject("WScript.Shell")
        lnkFile = "{file_o}"
        Set objLink = objWS.CreateShortcut(lnkFile)
        objLink.TargetPath = "{file_i}"
        objLink.Save
    ''').format(
        file_i=fs.abspath(file_i).replace('/', '\\'),
        file_o=fs.abspath(file_o).replace('/', '\\'),
    )
    dumps(command, vbs, ftype='plain')
    
    run_cmd_args('cscript', '/nologo', vbs)


def _fill_name(name: str, dir: str = None) -> str:
    # static
    name = (
        name
        .replace('{yyyy}', timestamp('y'))
        .replace('{mm}', timestamp('m'))
    )
    # dynamic
    if '{date}' in name:
        name = name.replace('{ver}', _find_latest_date(dir))
    if '{ver}' in name:
        name = name.replace('{ver}', _find_latest_version(dir))
    return name


def _find_latest_date(dir: str) -> str:
    for f in fs.find_dirs(dir):
        if re.match(r'\d{4}-\d{2}', f.name):
            return f.name
    raise FileNotFoundError


def _find_latest_version(dir: str) -> str:
    return fs.find_dir_names(dir)[-1]  # TODO


if __name__ == '__main__':
    # pox mypc_settings/make_shortcut.py
    main()
