import os
import sys
from textwrap import dedent

from lk_utils import call_once
from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads
from lk_utils import mklink
from lk_utils import run_cmd_args

from mypc_settings.common import reformat_path


@call_once()
def _change_dir_to_likianta_home() -> None:
    # noinspection PyCompatibility
    match sys.platform:
        case 'linux':
            os.chdir('/home/likianta/Desktop')
        case 'win32':
            os.chdir('C:/Likianta')  # TEST


def _load_config() -> dict:
    cfg_dir = fs.xpath('../config/shortcut_map')
    usr_dir = fs.xpath('../config/shortcut_map/user')
    match sys.platform:
        case 'win32':
            cfg = loads(f'{cfg_dir}/windows_shortcuts.yaml')
            if fs.exists(x := f'{usr_dir}/windows_shortcuts.yaml'):
                temp = loads(x)
                if temp.get('inherit', False):
                    cfg['map'].update(temp['map'])
                else:
                    cfg = temp
            return cfg
    raise NotImplementedError


def main() -> None:
    # root = 'shortcut'
    io_map = _load_config()['map']
    for i, o in io_map.items():
        i = reformat_path(i)
        if not fs.exists(i):
            print(':iv3', f'could not find "{i}"')
            continue
        
        if o == '...':
            o = 'shortcut/{}'.format(i.rsplit('/', 1)[-1])
        else:
            o = reformat_path(o)
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


if __name__ == '__main__':
    # pox mypc_settings/make_shortcut.py
    main()
