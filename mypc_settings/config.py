import os
import re
import sys
import typing as t
from functools import partial

from lk_utils import fs
from lk_utils import timestamp

home = ''


def load_config(file: str) -> dict:
    global home
    data = _load_config(file)
    home = data['home'] = _determine_home_directory(data)
    
    if 'alias' in data:
        # TODO: sort and deduplicate
        data['alias'] = _reformat_aliases(data['alias'])
    if 'environment' in data:
        data['environment'] = {
            k: tuple(map(reformat_path, (
                (v,) if isinstance(v, str) else
                (str(v),) if isinstance(v, int) else
                v  # list
            )))
            for k, v in data['environment'].items()
        }
    if 'shortcut' in data:
        data['shortcut'] = _reformat_shortcut_paths(data['shortcut'])
        data['shortcut'] = _deduplicate_shortcut_paths(data['shortcut'])
    return data


def _deduplicate_shortcut_paths(data: dict) -> dict:
    out = {}
    output_paths = []
    for k, v in reversed(data.items()):
        if v in output_paths:
            print('pop duplicate path: {} -> {}'.format(k, v), ':v7')
        else:
            out[k] = v
            output_paths.append(v)
    return out


def _determine_home_directory(config: dict) -> str:
    if 'home' in config:
        home = config['home']
    elif x := os.getenv('LIKIANTA_HOME'):
        home = x
    else:
        home = (
            '/Users/Likianta/Desktop' if sys.platform == 'darwin' else
            '/home/likianta/Desktop' if sys.platform == 'linux' else
            'C:/Likianta'  # win32
        )
    print(home, ':v2')
    assert home and home != '...' and fs.exist(home)
    return home


def _load_config(file: str) -> dict:
    data = fs.load(file)
    if 'inherit' not in data:
        return data
    
    # resolve inheritance
    x: str = data.pop('inherit')
    assert x != fs.basename(file)
    parent_file = '{}/{}'.format(fs.parent(file), x)
    assert fs.exist(parent_file)
    base = _load_config(parent_file)
    
    # print(base, ':vl')
    
    def inplace_nodes(node: dict, base: dict) -> dict:
        updated_node = {}
        for k, v in tuple(node.items()):
            # print(k, type(v), ':v')
            if k == '<inherit>':
                assert v is True or v == '...'
                updated_node.update(base)
                continue
            if isinstance(v, dict):
                assert isinstance(base[k], dict)
                updated_node[k] = inplace_nodes(v, base[k])
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
                updated_node[k] = temp
            else:
                updated_node[k] = v
        for k, v in base.items():
            if k not in node:
                updated_node[k] = v
        return updated_node
    
    data = inplace_nodes(data, base)
    return data


def _reformat_aliases(aliases: dict) -> dict:
    def _extend_replacement(item: str) -> str:
        return out[item]
    
    out = {}
    for k, v in aliases.items():
        out[k] = reformat_path(v, custom_replacer=_extend_replacement)
    return out


def _reformat_shortcut_paths(shortcuts: dict) -> dict:
    def _custom(basename: str, item: str) -> str:
        assert item == 'name_as_is'
        return basename
    
    out = {}
    for k, v in shortcuts.items():
        k = reformat_path(k)
        out[k] = reformat_path(
            v, custom_replacer=partial(_custom, fs.basename(k))
        )
    return out


def reformat_path(
    path: str,
    error_scheme: str = 'raise',
    custom_replacer: t.Optional[t.Callable[[str], str]] = None
) -> str:
    """
    errors: 'raise' or 'as_is'
    """
    
    def _inplace1(m: re.Match) -> str:
        item = m.group(1)
        # print(item, ':v')
        match item:
            case 'appdata':
                assert sys.platform == 'win32'
                return 'C:/Users/Likianta/AppData'
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
            # case 'scoop':
            #     assert sys.platform == 'win32'
            #     return 'C:/Users/Likianta/scoop'
            case 'shortcut':
                return f'{home}/shortcut'
            case 'start_menu':
                assert sys.platform == 'win32'
                return (
                    'C:/Users/Likianta/AppData/Roaming/Microsoft/Windows'
                    '/Start Menu'
                )
            case 'user_home':
                match sys.platform:
                    case 'darwin':
                        return '/Users/Likianta'
                    case 'linux':
                        return '/home/likianta'
                    case 'win32':
                        return 'C:/Users/Likianta'
            case 'yyyy':
                return timestamp('y')
            case _:
                if custom_replacer and (x := custom_replacer(item)):
                    return x
                else:
                    # others ('<date>', '<ver>', '<version>', etc.) are 
                    # "recursive" patterns, they require "parent_path" to be 
                    # evaluated first. 
                    # this function doesn't handle them. turn to `_inplace2()` 
                    # laterly.
                    return item
    
    path = re.sub(r'<(\w+)>', _inplace1, path)

    _parent = fs.parent(path)  # a dir path
    assert not re.search(r'<(\w+)>', _parent)

    def _inplace2(m: re.Match) -> str:
        item = m.group(1)
        match item:
            case 'date':
                return _find_latest_date(_parent)
            case 'ver':
                return _find_latest_version(_parent)
            case 'version':
                return _find_latest_version(_parent)
            case _:
                if error_scheme == 'as_is':
                    return m.group(0)
                else:
                    raise Exception(item)
    
    return re.sub(r'<(\w+)>', _inplace2, path)


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
