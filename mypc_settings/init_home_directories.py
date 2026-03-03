import os
from argsense import cli
from lk_utils import dedent
from lk_utils import fs
from lk_utils import timestamp


@cli.cmd()
def main(
    root: str, picture_classing_language='zh', extend: bool = True
    #   picture_classing_language: 'zh', 'zh_ex', 'en', 'en_ex'
) -> None:
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
        documents/tutorials
        documents/webclips
        documents/worksheets
        downloads
        other
        pictures
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
    match picture_classing_language:
        case 'zh':
            paths += '\n' + '收集'
        case 'zh_ex':
            paths += '\n' + dedent(
                '''
                pictures/壁纸
                pictures/壁纸/横屏
                pictures/壁纸/竖屏
                pictures/梗图
                pictures/梗图/热评 帖子 神对话
                pictures/其他
                pictures/其他/车祸 事故 灾难
                pictures/其他/恐怖
                pictures/其他/两性
                pictures/其他/猫猫以及各种动物
                pictures/其他/生活 人生
                pictures/收集
                pictures/头像
                pictures/我的
                pictures/我的/常理工
                pictures/我的/电子设备
                pictures/我的/工作
                pictures/我的/工作/开发日志
                pictures/我的/绘画
                pictures/我的/开车
                pictures/我的/美食拍拍拍
                pictures/我的/上海
                pictures/我的/实体娃娃
                pictures/我的/租房
                pictures/我的/租房/泊寓
                pictures/我的/租房/梅陇一村
                pictures/我的/租房/鹏裕苑
                pictures/我的/租房/禹州金桥
                # TODO...
                '''
            )
            raise NotImplementedError
        case 'en':
            paths += '\n' + 'Inbox'
        case 'en_ex':
            paths += '\n' + dedent(
                '''
                pictures/Inbox
                pictures/Other
                pictures/Wallpaper
                pictures/Wallpaper/Landscape
                pictures/Wallpaper/Portrait
                # TODO...
                '''
            )
            raise NotImplementedError
    if extend:
        paths += '\n' + dedent(
            '''
            apps/steam
            entertainment
            entertainment/comic
            entertainment/music
            entertainment/novel
            entertainment/video
            entertainment/video/short
            games
            nsfw
            nsfw/comics
            nsfw/footage
            nsfw/movies
            nsfw/other
            nsfw/pictures
            nsfw/unclassified
            other/wallpaper-slideshow
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
                airmise = { version = "^2.0.1a1", source = "likianta" }
                argsense = { version = "^1.1.1a0", source = "likianta" }
                faker = "^37.0.0"
                fastapi = { version = "^0.115.11", extras = ["standard"] }
                ipython = "^9.10.0"
                lk-logger = { version = ">=6.0.7,<6.1.0", source = "likianta" }
                lk-utils = { version = "^3.5.0a11", source = "likianta", \\
                extras = ["all"] }
                omni-driver-kit = { version = "^4.1.3a3", source = "likianta" }
                pyapp-window = { version = ">=2.1.5a5,<2.2.0", source = "likianta" }
                streamlit = "^1.54.0"
                streamlit-canary = { version = "^0.1.1a16", source = \\
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
                url = "http://localhost:2191/"
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
