import os

import lk_logger
from argsense import cli
from lk_utils import fs
from lk_utils import run_cmd_args

from mypc_settings import common


@cli.cmd()
def main(config_file: str = 'config/default.yaml') -> None:
    cfg = common.load_config(fs.abspath(config_file))
    for key, val in cfg['environment'].items():
        val = (
            ';'.join(val)
            .replace('/', '\\')
            .replace('http:\\\\', 'http://')
            .replace('https:\\\\', 'https://')
        )
        if os.environ.get(key) == val:
            print(key, val, ':v3s1')
        else:
            print(key, val, ':v4s1')
            with lk_logger.spinner(f'setting key: {key}'):
                run_cmd_args('setx', key, val)


if __name__ == '__main__':
    # pox mypc_settings/make_windows_user_environment_variables.py \
    #   config/user.yaml
    cli.run(main)
