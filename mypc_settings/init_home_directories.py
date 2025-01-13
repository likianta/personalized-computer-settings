from argsense import cli
from lk_utils import fs
from lk_utils.textwrap import dedent
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
        '''
    ).splitlines():
        print(p)
        match p:
            case 'pictures/Inbox/<auto>':
                fs.make_dir(f'{root}/{p}/{timestamp("yyyy")}')
            case 'temp/<auto>':
                fs.make_dir(f'{root}/{p}/{timestamp("yyyy-mm")}')
            case _:
                fs.make_dir(f'{root}/{p}')


if __name__ == '__main__':
    # pox mypc_settings/init_home_directories.py ...
    cli.run(main)
