from argsense import cli
from lk_utils import fs

from mypc_settings import common


@cli.cmd()
def main(
    config_file: str = fs.xpath('../config/dev_dist/map.yaml'),
) -> None:
    cfg = common.load_config(config_file)
    root = common.reformat_path(cfg['workspace_root'])
    print(root)
    for k, v in cfg['symlinks'].items():
        dir_i = common.reformat_path(k)
        dir_o = '{}/dev-dist/{}'.format(root, v)
        assert dir_i.endswith('/dist')
        common.print_conversion(fs.relpath(dir_i, root), f'dev_dist/{v}')
        if fs.exists(dir_i):
            fs.make_link(dir_i, dir_o)
        else:
            print('^   skip non-existent "dist" folder', ':vs')


if __name__ == '__main__':
    # pox mypc_settings/dev_dist.py
    cli.run(main)
