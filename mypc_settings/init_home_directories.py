from argsense import cli
from lk_utils import dedent
from lk_utils import fs
from lk_utils import timestamp


@cli.cmd()
def main(root: str) -> None:
    for p in dedent(
        '''
        applist
        apps
        apps/bore
        apps/dufs
        apps/flutter
        apps/jetbrains-toolbox
        apps/jetbrains-toolbox/apps
        apps/jetbrains-toolbox/scripts
        apps/nodejs
        apps/nushell
        apps/pypoetry
        apps/pypoetry/cache
        apps/python
        apps/python/3.8
        apps/python/3.9
        apps/python/3.10
        apps/python/3.11
        apps/python/3.12
        apps/python/3.13
        apps/qq
        apps/scoop
        apps/sogou-pinyin
        apps/wechat
        backups
        backups/android-apps
        backups/fonts
        backups/software-packages
        backups/software-settings
        documents
        documents/appdata
        documents/appdata/nushell
        documents/appdata/qq
        documents/appdata/wechat
        documents/gitbook
        documents/tutorials
        documents/worksheets
        downloads
        entertainment
        entertainment/comic
        entertainment/music
        entertainment/novel
        entertainment/video
        games
        nsfw
        other
        pictures
        pictures/Inbox
        pictures/Inbox/<auto>
        pictures/Wallpaper
        pictures/Wallpaper/Landscape
        pictures/Wallpaper/Portrait
        shortcut
        temp
        temp/<auto>
        temp/archived
        workspace
        workspace/archive
        workspace/com.jlsemi.likianta
        workspace/dev.master.likianta
        workspace/dev-dist
        workspace/playground
        workspace/playground/python-playground
        workspace/playground/python-playground/code
        workspace/playground/python-playground/data
        '''
    ).splitlines():
        print(p, ':s1')
        match p:
            case 'pictures/Inbox/<auto>':
                fs.make_dir('{}/{}'.format(
                    root, p.replace('<auto>', timestamp('y'))
                ))
            case 'temp/<auto>':
                fs.make_dir('{}/{}'.format(
                    root, p.replace('<auto>', timestamp('y-m'))
                ))
            case _:
                fs.make_dir(f'{root}/{p}')
    
    if not fs.exist(
        x := f'{root}/workspace/playground/python-playground/pyproject.toml'
    ):
        fs.dump(
            dedent(
                '''
                [tool.poetry]
                name = "python-playground"
                version = "0.0.0"
                description = ""
                authors = ["likianta <likianta@foxmail.com>"]
                # readme = "README.md"
                packages = [{ include = "code" }]
                
                [tool.poetry.dependencies]
                python = "^3.12"
                
                # --- A
                argsense = { version = "^0.6.4b1", source = "likianta-host" }
                ipython = "^8.31.0"
                lk-logger = { version = "^6.0.3", source = "likianta-host" }
                lk-utils = { version = "^3.1.3a2", source = "likianta-host" }
                streamlit = "^1.41.0"
                streamlit-canary = { version = "^0.1.0a14", source = \\
                "likianta-host" }
                
                # --- B
                # ...
                
                # --- C
                # ...
                
                [[tool.poetry.source]]
                name = "tsinghua"
                url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
                priority = "primary"
                
                [[tool.poetry.source]]
                name = "likianta-host"
                url = "http://likianta.pro:2131/"
                priority = "supplemental"
                
                [build-system]
                requires = ["poetry-core"]
                build-backend = "poetry.core.masonry.api"
                ''',
                join_sep='\\'
            ),
            x,
            'plain'
        )


if __name__ == '__main__':
    # pox mypc_settings/init_home_directories.py ...
    cli.run(main)
