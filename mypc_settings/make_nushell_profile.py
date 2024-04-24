import sys

from argsense import cli
from lk_utils import dumps
from lk_utils import fs
from lk_utils.textwrap import join

from mypc_settings import common


@cli.cmd()
def main(
    output_file: str =
    '{}/documents/appdata/nushell/likianta-profile.nu'.format(common.home),
    no_welcom_message: bool = False,
    config_file: str = fs.xpath(f'../config/shell/config_{sys.platform}.yaml'),
) -> None:
    cfg = common.loads_config(fs.abspath(config_file))
    platform = sys.platform  # 'darwin', 'linux', 'win32'
    assert platform in ('darwin', 'linux', 'win32')
    
    output = [
        '# this file is auto generated/updated by {}'.format(
            '[make_nushell_profile.py](https://github.com/likianta/personal'
            '-settings/blob/main/mypc_settings/make_nushell_profile.py)'
        ),
        '$env.config.show_banner = false' if no_welcom_message else '',
        '$env.PROMPT_COMMAND = {{|| $env.PWD | split row "{}" | last }}'
        .format('/' if platform != 'win32' else '\\\\'),
        # do not show timestamp on right prompt in windows, because it may be -
        # chinese sans-serif font which looks not good.
        '$env.PROMPT_COMMAND_RIGHT = ""' if platform == 'win32' else '',
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
    
    dumps(output, output_file, 'plain')
    print(f'file is saved to "{output_file}"')


if __name__ == '__main__':
    # pox mypc_settings/make_nushell_profile.py
    # pox mypc_settings/make_nushell_profile.py <custom_file>
    cli.run(main)
