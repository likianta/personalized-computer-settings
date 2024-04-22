# `config` Folder Structure

tree:

```
config
|= shell
    |- config.yaml
    |- config_darwin.yaml
    |- config_linux.yaml
    |- config_win32.yaml
|= shortcut_map
    |- shortcut.yaml
    |- shortcut_darwin.yaml
    |- shortcut_linux.yaml
    |- shortcut_win32.yaml
```

'config.yaml' is default config, 'config_darwin.yaml' etc. is platform specific config.

`mypc_settings/common.py` will merge them by `<inherit>` keyword.

for example:

```
default         platform specific       merged result
------------    ------------------      -------------
aaa: bbb        aaa: kkk                aaa: kkk
ccc:            ccc:                    ccc:
    - ddd           - <inherit>             - ddd
    - eee           - lll                   - eee
                    - mmm                   - lll
                                            - mmm
fff:            fff:                    fff:
    ggg: hhh        <inherit>: ...          ggg: hhh
    iii: jjj        iii: nnn                iii: nnn
                    ooo: ppp                ooo: ppp
```
