import sys
import typing as t

from argsense import cli
from lk_utils import fs
from lk_utils import timestamp
from lk_utils.textwrap import join

from mypc_settings import load_config
from mypc_settings import reformat_path


@cli.cmd()
def main(
    config_file: str = 'config/default.yaml',
    output_file: str = '<home>/documents/appdata/nushell/likianta-profile.nu',
    environment_settings_scheme: str = 'nushell',
    enable_starship: bool = False,
    hide_welcome_message: t.Optional[bool] = None,
) -> None:
    """
    kwargs:
        environment_settings_scheme (-e): 'nushell', 'windows', 'ignore'
            'nushell': output environment settings to `output_file`.
            'windows': set environment variables in windows.
            'ignore': do nothing.
    """
    cfg = load_config(fs.abspath(config_file))
    output_file = reformat_path(output_file)
    platform = sys.platform  # 'darwin', 'linux', 'win32'
    assert platform in ('darwin', 'linux', 'win32')
    
    output = [
        '# this file is auto generated/updated by {}'.format(
            '[make_nushell_profile.py](https://github.com/likianta/personal'
            '-settings/blob/main/mypc_settings/make_nushell_profile.py)'
        ),
        '# file was updated at {}'.format(timestamp('y-m-d h:m:s')),
        '',
        '$env.LIKIANTA_HOME = "{}"'.format(cfg['home']),
        '',
    ]
    
    # env vars
    match environment_settings_scheme:
        case 'ignore':
            print('ignore environment settings', ':vs')
        case 'nushell':
            for key, val in cfg['environment'].items():
                if key == 'PATH':
                    output.append('$env.{} = [\n    {}\n]'.format(
                        key, join((f'"{x}",' for x in val), 4)
                    ))
                else:
                    output.append('$env.{} = "{}"'.format(key, ';'.join(val)))
            output.append('')
        case 'windows':
            assert platform == 'win32'
            from mypc_settings import make_windows_user_environment_variables
            make_windows_user_environment_variables.main(config_file)
    
    # alias
    for key, val in cfg['alias'].items():
        print(f'{key} -> {val}', ':r2')
        output.append('alias {} = {}'.format(key, val))
    output.append('')
    
    if enable_starship:
        # https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship
        if not fs.exists(
            x := f'{cfg["home"]}/documents/appdata/nushell/starship-init.nu'
        ):
            print('''
                "starship-init.nu" is not created. use the following command -
                to create it (in your nushell):
                    starship init nu | save {}
            '''.format(x))
            exit()
        output.append('use {}'.format(x))
    else:
        output.extend((
            '$env.PROMPT_COMMAND = {{|| $env.PWD | split row "{}" | last }}'
            .format('/' if platform != 'win32' else '\\\\'),
            # do not show timestamp on right prompt in windows, because it may -
            # be chinese sans-serif font which looks not good.
            '$env.PROMPT_COMMAND_RIGHT = ""' if platform == 'win32' else '',
        ))
    output.append('')
    
    if hide_welcome_message:
        print('''
            please manually edit `$nu.config-path` to disable the banner of -
            welcome message:
                1. search "show_banner"
                2. set it to `false`
        ''')
    
    fs.dump(output, output_file, 'plain')
    print(f'file is saved to "{output_file}"')


if __name__ == '__main__':
    # pox mypc_settings/make_nushell_profile.py
    # pox mypc_settings/make_nushell_profile.py --config-file
    #   config/shell/map_win32_user.yaml -e windows
    # pox mypc_settings/make_nushell_profile.py --config-file
    #   config/shell/map_win32_user.yaml -e ignore
    cli.run(main)
