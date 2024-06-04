from argsense import cli
from lk_utils import fs, run_cmd_args

from mypc_settings import common


@cli.cmd()
def main(
    config_file: str = fs.xpath(f'../config/shell/map_win32.yaml'),
) -> None:
    cfg = common.loads_config(fs.abspath(config_file))
    for key, val in cfg['environment'].items():
        val = ';'.join(val).replace('/', '\\').replace('http:\\\\', 'http://')
        print(key, val)
        run_cmd_args('setx', key, val, verbose=True)


if __name__ == '__main__':
    # pox mypc_settings/make_windows_user_environment_variables.py
    # pox mypc_settings/make_windows_user_environment_variables.py
    #   config/shell/map_win32_user.yaml
    cli.run(main)
