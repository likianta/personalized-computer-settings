import os

from argsense import cli
from lk_utils import dumps
from lk_utils import fs
from lk_utils import timestamp

from mypc_settings import common


@cli.cmd()
def main(
    config_file: str = fs.xpath(f'../config/shell/map_win32.yaml'),
    output_file: str = (
        '{}/Documents/PowerShell/Microsoft.PowerShell_profile.ps1'
        .format(os.environ['USERPROFILE'].replace('\\', '/'))
    ),
    enable_ohmyposh: bool = False,
    enable_starship: bool = False,
    enter_nushell: bool = False,
) -> None:
    cfg = common.loads_config(config_file)
    output = [
        '# this file is auto generated by [prj] '
        'personalized-computer-settings : mypc_settings/'
        'make_powershell_profile.py',
        '# file was updated at {}'.format(timestamp('y-m-d h:m:s')),
        '',
    ]
    
    # env vars
    for key, val in cfg['environment'].items():
        output.append('Set-Item -Path env:{} -Value "{}"'.format(
            key, ';'.join(val)
        ))
    output.append('')
    
    # alias
    for key, val in cfg['alias'].items():
        common.print_conversion(key, val)
        # output.append('New-Alias -Name {} -Value "{}"'.format(key, val))
        output.append('function {} {{ {} $args }}'.format(key, val))
        #   https://stackoverflow.com/a/4167071
    output.append('')
    
    if enable_ohmyposh:
        output.append('oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\\'
                      'amro.omp.json | Invoke-Expression')
    if enable_starship:
        # background:
        #   scoop install starship
        #   # ^ check its installation log.
        output.append('Invoke-Expression (&starship init powershell)')
    if enter_nushell:
        output.append('C:/Likianta/apps/nushell/nu.exe')
    
    dumps(output, output_file, 'plain')


if __name__ == '__main__':
    # pox mypc_settings/make_powershell_profile.py
    # pox mypc_settings/make_powershell_profile.py --enable-ohmyposh
    # pox mypc_settings/make_powershell_profile.py --enable-starship
    cli.run(main)
