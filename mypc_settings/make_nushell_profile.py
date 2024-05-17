import sys
import typing as t

from argsense import cli
from lk_utils import dumps
from lk_utils import fs
from lk_utils import timestamp
from lk_utils.textwrap import join

from mypc_settings import common


@cli.cmd()
def main(
    output_file: str =
    '{}/documents/appdata/nushell/likianta-profile.nu'.format(common.home),
    config_file: str = fs.xpath(f'../config/shell/map_{sys.platform}.yaml'),
    enable_starship: bool = False,
    hide_welcome_message: t.Optional[bool] = None,
) -> None:
    cfg = common.loads_config(fs.abspath(config_file))
    platform = sys.platform  # 'darwin', 'linux', 'win32'
    assert platform in ('darwin', 'linux', 'win32')
    
    output = [
        '# this file is auto generated/updated by {}'.format(
            '[make_nushell_profile.py](https://github.com/likianta/personal'
            '-settings/blob/main/mypc_settings/make_nushell_profile.py)'
        ),
        '# file was updated at {}'.format(timestamp('y-m-d h:m:s')),
        '',
        '$env.LIKIANTA_HOME = "{}"'.format(common.home),
        '',
    ]
    
    # env vars
    for key, val in cfg['environment'].items():
        if key == 'PATH':
            output.append('$env.{} = [\n    {}\n]'.format(
                key, join((f'"{x}",' for x in val), 4)
            ))
        else:
            output.append('$env.{} = "{}"'.format(key, ';'.join(val)))
    output.append('')
    
    # alias
    for key, val in cfg['alias'].items():
        common.print_conversion(key, val)
        output.append('alias {} = {}'.format(key, val))
    output.append('')
    
    if enable_starship:
        # https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship
        if not fs.exists(
            x := f'{common.home}/documents/appdata/nushell/starship-init.nu'
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
    
    dumps(output, output_file, 'plain')
    print(f'file is saved to "{output_file}"')


if __name__ == '__main__':
    # pox mypc_settings/make_nushell_profile.py
    # pox mypc_settings/make_nushell_profile.py --config-file
    #   config/shell/map_win32_user.yaml
    # pox mypc_settings/make_nushell_profile.py <custom_file>
    # pox mypc_settings/make_nushell_profile.py --enable-starship
    cli.run(main)
