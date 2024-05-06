import os

import lk_logger
from argsense import cli

lk_logger.setup()


@cli.cmd()
def main(key: str = None) -> None:
    if key is None:
        origin = input('input paths to be sort: ')
    else:
        origin = os.environ[key]
    paths = [
        x.replace('/', '\\').rstrip('\\')
        for x in origin.split(';') if x
    ]
    paths.sort(key=_sort)
    print(paths, ':l')
    print(';'.join(paths))


def _sort(path: str) -> tuple[int, str]:
    if path.startswith('%'):
        return 1, path
    else:
        return 0, path


if __name__ == '__main__':
    # pox mypc_settings/sort_windows_environment_paths.py
    # pox mypc_settings/sort_windows_environment_paths.py PATH
    cli.run(main)
