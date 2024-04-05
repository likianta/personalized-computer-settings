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


def main() -> None:
    root = 'shortcut'
    # noinspection PyCompatibility
    match sys.platform:
        case 'linux':
            i = _get_latest_temp_folder()
            o = '{}/temp-({})'.format(root, i.split('/')[-1])
            if not fs.exists(o):
                for d in fs.find_dirs(root):
                    if d.name.startswith('temp-('):
                        print(
                            'replace old temp folder "{}" with new: "{}"'
                            .format(d.name, fs.basename(o))
                        )
                        fs.remove_file(d.path)
                        break
                print('{} -> {}'.format(i, o), ':iv2')
                mklink(i, o)


def _get_latest_temp_folder() -> str:
    out = 'temp/{}'.format(timestamp('y-m'))  # e.g. 'temp/2024-04'
    if not fs.exists(out):
        fs.make_dir(out)
    return out


if __name__ == '__main__':
    # pox mypc_settings/make_shortcut.py
    main()
