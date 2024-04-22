
## Global Variables

> related module: `mypc_settings/common.py : reformat_path : inplace`

- `<appdata>`

    windows only, points to `C:/Users/Likianta/AppData` folder.

- `<desktop>`

    points to `~/Desktop` folder.

- `<home>`

    exclusive directory for likianta. OS biased:

    - linux: `/home/likianta/Desktop`
    - macos: `/Users/Likianta/Desktop`
    - windows: `C:/Likianta`

    this directory is fully controlled by likianta, it doesn't allow any other program to abuse of spamming files in the its top folders structure.

- `<mm>`

    current month, e.g. "04".

- `<start_menu>`

    windows only, points to `C:/Users/Likianta/AppData/Roaming/Microsoft/Windows/Start Menu` folder.

- `<user_home>`

    general user home directory, OS biased:

    - linux: `/home/likianta`
    - macos: `/Users/Likianta`
    - windows: `C:/Users/Likianta`

- `<yyyy>`

    current year, e.g. "2024".
