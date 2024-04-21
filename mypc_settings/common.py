import re
import sys
import typing as t

from lk_utils import fs
from lk_utils import timestamp


def print_conversion(*args: str) -> None:
    title, old, new = ('', *args)[-3:]
    print('{}[red]{}[/] -> [green]{}[/]'.format(
        title and title + ': ', old, new
    ), ':i2pr')


def reformat_path(
    path: str,
    errors: str = 'raise',
    custom_replacer: t.Callable[[str], str] = None
) -> str:
    """
    errors: 'raise' or 'as-is'
    """
    _parent = fs.parent(path)  # a dir path
    
    def inplace(m: re.Match) -> str:
        item = m.group(1)
        match item:
            case 'date':
                return _find_latest_date(_parent)
            case 'home':
                match sys.platform:
                    case 'darwin':
                        return '/Users/Likianta/Desktop'
                    case 'linux':
                        return '/home/likianta/Desktop'
                    case 'win32':
                        return 'C:/Likianta'
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
                    return ('C:/Users/Likianta/AppData/Roaming/Microsoft/'
                            'Windows/Start Menu')
                case 'user_home':
                    return 'C:/Users/Likianta'
        
        if custom_replacer and (x := custom_replacer(item)):
            return x
        
        if errors == 'as-is':
            return m.group(0)
        else:
            raise Exception(item)
    
    return re.sub(r'<(\w+)>', inplace, path)


def _find_latest_date(dir: str) -> str:
    for f in fs.find_dirs(dir):
        if re.match(r'\d{4}-\d{2}', f.name):
            return f.name
    raise FileNotFoundError


def _find_latest_version(dir: str) -> str:
    return fs.find_dir_names(dir)[-1]  # TODO
