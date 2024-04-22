import re
import sys
import typing as t

from lk_utils import fs
from lk_utils import loads
from lk_utils import timestamp


def loads_config(path: str) -> dict:
    data = loads(path)
    # TODO: sort and deduplicate
    data['alias'] = reformat_aliases(data['alias'])
    data['environment'] = {
        k: map(reformat_path, ((v,) if isinstance(v, str) else v))
        for k, v in data['environment'].items()
    }
    return data


def print_conversion(*args: str) -> None:
    title, old, new = ('', *args)[-3:]
    print('{}[red]{}[/] -> [green]{}[/]'.format(
        title and title + ': ', old, new
    ), ':i2pr')


def reformat_aliases(aliases: dict) -> dict:
    def _extend_replace(item: str) -> str:
        return out[item]
    
    out = {}
    for k, v in aliases.items():
        out[k] = reformat_path(v, custom_replacer=_extend_replace)
    return out


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
            case 'desktop':
                match sys.platform:
                    case 'darwin':
                        return '/Users/Likianta/Desktop'
                    case 'linux':
                        return '/home/likianta/Desktop'
                    case 'win32':
                        return 'C:/Users/Likianta/Desktop'
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
            case 'user_home':
                match sys.platform:
                    case 'darwin':
                        return '/Users/Likianta'
                    case 'linux':
                        return '/home/likianta'
                    case 'win32':
                        return 'C:/Users/Likianta'
        
        if sys.platform == 'win32':
            match item:
                case 'appdata':
                    return 'C:/Users/Likianta/AppData'
                case 'start_menu':
                    return ('C:/Users/Likianta/AppData/Roaming/Microsoft/'
                            'Windows/Start Menu')
        
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
    ver_pattern = re.compile(r'[0-9][.0-9]+')
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
