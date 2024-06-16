from argsense import cli
from lk_utils import fs
from lk_utils.textwrap import dedent
from lk_utils import timestamp


@cli.cmd()
def main(root: str) -> None:
    for p in dedent('''
        applist
        apps
        apps/bandizip
        apps/jetbrains-toolbox
        apps/jetbrains-toolbox/apps
        apps/jetbrains-toolbox/scripts
        apps/nodejs
        apps/nushell
        apps/pypoetry
        apps/python
        apps/python/3.8
        apps/python/3.12
        apps/qq
        apps/scoop
        apps/sogou-pinyin
        apps/steam
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
        shortcut
        temp
        temp/archived
        workspace
        workspace/archive
        workspace/dev-dist
        workspace/likianta.founder.pro
        workspace/likianta.jlsemi.com
        workspace/likianta.master.dev
        workspace/playground
        workspace/playground/python-playground
    ''').splitlines():
        print(p)
        fs.make_dir(f'{root}/{p}')
        if p == 'temp':
            fs.make_dir(f'{root}/{p}/{timestamp("yyyy-mm")}')


if __name__ == '__main__':
    # pox mypc_settings/init_home_directories.py ...
    cli.run(main)
