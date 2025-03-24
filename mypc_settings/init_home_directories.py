from argsense import cli
from lk_utils import dedent
from lk_utils import fs
from lk_utils import timestamp


@cli.cmd()
def main(root: str, extend: bool = True) -> None:
    paths = dedent(
        '''
        applist
        apps
        apps/android
        apps/android/sdk
        apps/bore
        apps/clash-nyanpasu
        apps/depsland
        apps/dufs
        apps/flutter
        apps/git
        apps/jetbrains-toolbox
        apps/jetbrains-toolbox/apps
        apps/jetbrains-toolbox/scripts
        apps/netease-cloud-music
        apps/nodejs
        apps/nodejs/globals
        apps/nodejs/globals/cache
        apps/nodejs/globals/modules
        apps/nodejs/node
        apps/nodejs/pnpm
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
        apps/qq-pc-manager
        apps/scoop
        apps/sogou-pinyin
        apps/sunlogin
        apps/typora
        apps/visual-studio
        apps/visual-studio/packages
        apps/visual-studio/shared
        apps/visual-studio/vs-community-2022
        apps/vscode
        apps/wechat
        apps/wps-office
        apps/xyplorer-free
        backups
        backups/android-apps
        backups/fonts
        backups/software-packages
        backups/software-settings
        backups/unclassified
        documents
        documents/appdata
        documents/appdata/flutter
        documents/appdata/flutter/pub-cache
        documents/appdata/nushell
        documents/appdata/pixcall
        documents/appdata/pixcall/MyPictures
        documents/appdata/qq
        documents/appdata/wechat
        documents/gitbook
        documents/tutorials
        documents/worksheets
        downloads
        other
        pictures
        pictures/Inbox
        pictures/Inbox/<auto>
        pictures/Wallpaper
        shortcut
        temp
        temp/<auto>
        temp/archived
        workspace
        workspace/archived
        workspace/com.jlsemi.likianta
        workspace/creative-studio
        workspace/dev.master.likianta
        workspace/playground
        workspace/playground/python-playground
        workspace/playground/python-playground/code
        workspace/playground/python-playground/data
        '''
    )
    if extend:
        paths += '\n' + dedent(
            '''
            apps/steam
            entertainment
            entertainment/comic
            entertainment/music
            entertainment/novel
            entertainment/video
            games
            nsfw
            nsfw/comics
            nsfw/footage
            nsfw/movies
            nsfw/other
            nsfw/pictures
            nsfw/unclassified
            '''
        )
    
    for p in paths.splitlines():
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
    
    # -------------------------------------------------------------------------
    
    if not fs.exist(x := f'{root}/pictures/Pixcall'):
        fs.make_link(f'{root}/documents/appdata/pixcall/MyPictures', x)
    
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
                argsense = { version = "^0.6.4", source = "likianta" }
                ipython = "^8.31.0"
                lk-logger = { version = "^6.0.3", source = "likianta" }
                lk-utils = { version = "^3.1.3a3", source = "likianta" }
                streamlit = "^1.41.0"
                streamlit-canary = { version = "^0.1.0a14", source = "likianta" }
                
                # --- B
                # ...
                
                # --- C
                # ...
                
                [[tool.poetry.source]]
                name = "tsinghua"
                url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
                priority = "primary"
                
                [[tool.poetry.source]]
                name = "likianta"
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
