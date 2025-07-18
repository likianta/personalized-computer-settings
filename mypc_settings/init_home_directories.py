import os
from argsense import cli
from lk_utils import dedent
from lk_utils import fs
from lk_utils import timestamp


@cli.cmd()
def main(root: str, extend: bool = True) -> None:
    paths = dedent(
        '''
        # <applist>
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
        apps/python/3.14
        apps/qq
        apps/qq-pc-manager
        apps/rust
        apps/rust/cargo
        apps/rust/rust
        apps/rust/rustup
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
        # documents/notebook
        documents/tutorials
        documents/webclips
        documents/worksheets
        downloads
        other
        pictures
        pictures/Inbox
        pictures/Inbox/<auto>
        pictures/Unclassified
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
        workspace/playground/rust-playground
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
        if p.startswith('#'):
            continue
        match p:
            case '<applist>':
                fs.make_shortcut(
                    os.path.expanduser('~/Desktop'),
                    '{}/applist.lnk'.format(root)
                )
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
    
    # if not fs.exist(x := f'{root}/pictures/Pixcall'):
    #     fs.make_link(f'{root}/documents/appdata/pixcall/MyPictures', x)
    
    if not fs.exist(
        x := f'{root}/workspace/playground/python-playground/pyproject.toml'
    ):
        fs.dump(
            dedent(
                '''
                [project]
                name = "python-playground"
                version = "0.0.0"
                description = ""
                authors = [{ name = "Likianta", email = \\
                "likianta@foxmail.com" }]
                packages = [{ include = "code" }]
                requires-python = ">=3.12"
                dynamic = ["dependencies"]
                
                [tool.poetry.dependencies]
                python = "^3.12"
                
                # --- A
                airmise = { version = "^0.4.0b1", source = "likianta" }
                argsense = { version = "^1.0.1b1", source = "likianta" }
                faker = "^37.0.0"
                fastapi = { version = "^0.115.11", extras = ["standard"] }
                ipython = "^9.4.0"
                lk-logger = { version = "^6.0.7a0", source = "likianta" }
                lk-utils = { version = "^3.3.0a16", source = "likianta", \\
                extras = ["all"] }
                omni-driver-kit = { version = "^4.1.0a11", source = "likianta" }
                pyapp-window = { version = "^2.2.0b4", source = "likianta" }
                streamlit = "^1.45.0"
                streamlit-canary = { version = "^0.1.0b10", source = \\
                "likianta" }
                
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
                url = "http://localhost:2131/"
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
