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


def _load_config() -> dict:
    cfg_dir = fs.xpath('../config')
    usr_dir = fs.xpath('../config/user')
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
        i = finish_path(i)
        if not fs.exists(i):
            print(':iv3', f'could not find "{i}"')
            continue
        
        if o == '...':
            o = 'shortcut/{}'.format(i.rsplit('/', 1)[-1])
        else:
            o = finish_path(o)
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


def finish_path(path: str) -> str:
    _parent = fs.parent(path)  # a dir path
    
    def inplace(m: re.Match) -> str:
        item = m.group(1)
        match item:
            case 'date':
                return _find_latest_date(_parent)
            case 'mm':
                return timestamp('m')
            case 'yyyy':
                return timestamp('y')
            case 'ver':
                return _find_latest_version(_parent)
        
        if sys.platform == 'win32':
            match item:
                case 'appdata':
                    return 'C:/Users/Likianta/AppData'
                case 'start_menu':
                    return 'C:/Users/Likianta/AppData/Roaming/Microsoft/Windows/Start Menu'
                case 'user_home':
                    return 'C:/Users/Likianta'
        
        raise Exception(item)
    
    return re.sub(r'<(\w+)>', inplace, path)


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
