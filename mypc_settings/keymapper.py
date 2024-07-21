from argsense import cli
from lk_utils import fs


@cli.cmd()
def ahk(
    rctrl_to_change_ime: bool = False,
    rshift_to_underscore: bool = True,
    swap_single_and_double_quotes: bool = False,
) -> None:
    output = []
    
    if rctrl_to_change_ime:
        output.extend((
            '; rctrl = ctrl + space',
            'RControl::Send "^{Space}"',
            'RControl & *::Send "^*"',
            '',
        ))
    
    if rshift_to_underscore:
        output.extend((
            '; rshift = underscore',
            'RShift::SendText "_"',
            'RShift & *::Send "{RShift} & *"',
            '',
        ))
    
    if swap_single_and_double_quotes:
        # https://www.autohotkey.com/docs/v2/howto/SendKeys.htm
        output.extend((
            '; swap single and double quotes',
            '\'::SendText \'"\'',
            '+\'::SendText "\'"',
            '',
        ))
    
    fs.dump(output, fs.xpath('../config/keymap.ahk'))


if __name__ == '__main__':
    # pox mypc_settings/keymapper.py ahk
    cli.run()
