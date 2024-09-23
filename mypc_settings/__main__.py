import sys

from argsense import cli

from .config import load_config


@cli.cmd()
def preview_config(file: str) -> None:
    print(':l', load_config(file))
    
    
@cli.cmd()
def setup(
    file: str = 'config/default.yaml',
    overwrite_shortcuts: bool = False
) -> None:
    # config = load_config(file)
    
    from .make_nushell_profile import main
    main(
        file,
        environment_settings_scheme='windows'
        if sys.platform == 'win32' else 'nushell'
    )
    
    from .make_shortcut import main
    main(file, overwrite_shortcuts)


if __name__ == '__main__':
    # pox -m mypc_settings preview-config config/default.yaml
    # pox -m mypc_settings preview-config config/user.yaml
    # pox -m mypc_settings setup config/user.yaml
    cli.run()
