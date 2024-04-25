import os
import re
import sys
import typing as t

from lk_utils import fs
from lk_utils import loads
from lk_utils import timestamp

if x := os.getenv('LIKIANTA_HOME'):
    home = x
else:
    home = (
        '/Users/Likianta/Desktop' if sys.platform == 'darwin' else
        '/home/likianta/Desktop' if sys.platform == 'linux' else
        'C:/Likianta'  # win32
    )


def loads_config(file: str) -> dict:
    data = _loads_config(file)
    if 'alias' in data:
        # TODO: sort and deduplicate
        data['alias'] = reformat_aliases(data['alias'])
    if 'environment' in data:
        data['environment'] = {
            k: map(reformat_path, ((v,) if isinstance(v, str) else v))
            for k, v in data['environment'].items()
        }
    if 'map' in data:
        data['map'] = {
            reformat_path(k): reformat_path(v)
            for k, v in data['map'].items()
        }
    return data


def _loads_config(file: str) -> dict:
    data = loads(file)
    if 'inherit' not in data:
        return data
    
    # resolve inheritance
    x = data.pop('inherit')
    assert x is True or isinstance(x, str)
    #   `x` is either True or a string of path.
    #   if it is True, will guess its base config from its file name.
    #   if it a path string, will find the filename in the same dir.
    if x is True:
        a, b, c = fs.split(file, 3)
        assert '_' in b
        parent_file = '{}/{}.{}'.format(a, b.rsplit('_', 1)[0], c)
    else:
        assert x != fs.basename(file)
        parent_file = '{}/{}'.format(fs.parent(file), x)
    assert fs.exists(parent_file)
    base = _loads_config(parent_file)
    # print(base, ':vl')
    
    def inplace_nodes(node: dict, base: dict) -> dict:
        for k, v in tuple(node.items()):
            # print(k, type(v), ':v')
            if k == '<inherit>':
                node.update(base)
                continue
            if isinstance(v, dict):
                assert isinstance(base[k], dict)
                inplace_nodes(v, base[k])
            elif isinstance(v, list):
                temp = []
                for x in v:
                    assert isinstance(x, str)
                    if x == '<inherit>':
                        # print(k, v, base[k], ':vl')
                        assert isinstance(base[k], list)
                        temp.extend(base[k])
                    else:
                        temp.append(x)
                node[k] = temp
            else:
                continue
        for k, v in base.items():
            if k not in node:
                node[k] = v
        return node
    
    data = inplace_nodes(data, base)
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
                return home
            case 'mm':
                return timestamp('m')
            case 'shortcut':
                return f'{home}/shortcut'
            case 'user_home':
                match sys.platform:
                    case 'darwin':
                        return '/Users/Likianta'
                    case 'linux':
                        return '/home/likianta'
                    case 'win32':
                        return 'C:/Users/Likianta'
            case 'ver':
                return _find_latest_version(_parent)
            case 'yyyy':
                return timestamp('y')
        
        if sys.platform == 'win32':
            match item:
                case 'appdata':
                    return 'C:/Users/Likianta/AppData'
                # case 'scoop':
                #     return 'C:/Users/Likianta/scoop'
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
