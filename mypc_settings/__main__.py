import sys

from argsense import cli

from . import init_home_directories
from .config import load_config

cli.add_cmd(init_home_directories.main, 'init-home-dirs')


@cli.cmd('preview')
def preview_config(file: str) -> None:
    print(':l', load_config(file))
    
    
@cli.cmd()
def setup(
    file: str = 'config/default.yaml',
    overwrite_shortcuts: bool = False,
    clean_shortcuts: bool = False,
) -> None:
    """
    after setup, don't forget to add this line to the bottom of nushell's -
    config path (`$nu.config-path`):
        source <home>/documents/appdata/nushell/likianta-profile.nu
    
    params:
        overwrite_shortcuts (-o):
        clean_shortcuts (-c):
    """
    # config = load_config(file)
    
    from .make_nushell_profile import main
    main(
        file,
        environment_settings_scheme='windows'
        if sys.platform == 'win32' else 'nushell'
    )
    
    from .make_shortcut import main
    main(file, overwrite_shortcuts, clean_shortcuts)


if __name__ == '__main__':
    # pox -m mypc_settings -h
    # pox -m mypc_settings init-home-dirs C:/Likianta :true
    # pox -m mypc_settings preview config/default.yaml
    # pox -m mypc_settings preview config/user.yaml
    # pox -m mypc_settings setup config/user.yaml
    # pox -m mypc_settings setup config/user.yaml -o
    cli.run()
