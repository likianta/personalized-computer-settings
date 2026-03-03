import os

if 'BORE_SECRET' not in os.environ:
    raise Exception('set BORE env first.')

import re
import typing as t
from collections import defaultdict

import psutil
import streamlit as st
import streamlit_canary as sc
from lk_utils import fs
from lk_utils import run_cmd_line
from lk_utils.subproc import Popen


def _init() -> dict:
    """
    returns:
        {'config': dict, 'running_tasks': dict tasks}
            tasks: {str key: [(Popen object | int pid), ...], ...}
    """
    if 'VIRTUAL_ENV' in os.environ:
        del os.environ['VIRTUAL_ENV']
    return {
        'config': fs.load(fs.xpath('config.yaml')),
        'running_tasks': defaultdict(list)
    }


state = sc.init_state(_init, version=5)


def main() -> None:
    cols = st.columns(4)
    for i, item in enumerate(state['config']):
        with cols[i % 4]:
            with sc.card(item['name']):
                key = item['name']
                help_text = (
                    '`{}`'.format(item['cmd'])
                    if isinstance(item['cmd'], str)
                    else '\n'.join(f'- `{x}`' for x in item['cmd'])
                )
                
                with sc.row():
                    if key in state['running_tasks']:
                        _stop_button(key, help_text)
                    else:
                        _start_button(item, key, help_text)
                    _command_edit_button(key)
    
    st.divider()
    with sc.row():
        if st.button('Reload config'):
            state['config'] = fs.load(fs.xpath('config.yaml'))
            st.rerun()
        if st.button('Restore sessions'):
            _restore_running_tasks()
            st.rerun()


def _command_edit_button(key):
    if st.button(
        '⚙️',  # https://getemoji.com/
        key='{}:edit'.format(key),
        help='Edit the command. :red[(Not implemented)]',
    ):
        pass


def _start_button(item, key, help_text):
    if st.button(
        'Run',
        key='{}:run'.format(key),
        help=help_text,
        width='stretch',
    ):
        if isinstance(item['cmd'], str):
            cmd_list = (item['cmd'],)
        else:
            cmd_list = item['cmd']
        cwd = item.get('cwd')
        for cmd in cmd_list:
            process = _run_command(cmd, cwd)
            state['running_tasks'][key].append(process)
        # backup to local disk in case session destroyed.
        _backup_running_tasks()
        st.rerun()


def _stop_button(key, help_text):
    if st.button(
        'Stop',
        key='{}:stop'.format(key),
        help=help_text,
        width='stretch',
        type='primary',  # red bg
    ):
        xlist = state['running_tasks'].pop(key)
        for x in xlist:
            if isinstance(x, Popen):
                x.kill()
            else:
                pid = x
                parent = psutil.Process(pid)
                print(
                    ':v7',
                    'kill process: {} ({})'.format(
                        pid, parent.name()
                    )
                )
                for child in parent.children(recursive=True):
                    print(
                        ':v7',
                        '|- kill child process: {} ({})'.format(
                            child.pid, child.name()
                        )
                    )
                    # noinspection PyUnresolvedReferences
                    try:
                        child.kill()
                    except psutil.NoSuchProcess:
                        pass
                # noinspection PyUnresolvedReferences
                try:
                    parent.kill()
                except psutil.NoSuchProcess:
                    pass
        st.rerun()

# ------------------------------------------------------------------------------

def _backup_running_tasks() -> None:
    data = {}
    for key, proc_list in state['running_tasks'].items():
        data[key] = [proc.pid for proc in proc_list]
    fs.dump(data, fs.xpath('_running_tasks.json'))


def _restore_running_tasks() -> None:
    data = fs.load(fs.xpath('_running_tasks.json'))
    for key, pids in data.items():
        if key in state['running_tasks']:
            print(':v6l', 'cannot restore backed task', key, pids)
        else:
            state['running_tasks'][key] = pids


def _run_command(cmd: str, cwd: t.Optional[str]) -> Popen:
    assert 'VIRTUAL_ENV' not in os.environ
    cmd = _inplace_variables(cmd)
    if cwd: cwd = cwd.replace('<likianta>', 'C:/Likianta')
    print(cmd, cwd, ':v2l')
    return run_cmd_line(
        cmd, cwd=cwd, blocking=False, verbose=True, force_term_color=True
    )


def _inplace_variables(cmd: str) -> str:
    
    def _inplace(m: re.Match) -> str:
        match m.group(1):
            case 'bore':
                return (
                    'bore local -s {bore_secret} -t {public_ip}'.format(
                        bore_secret=os.environ['BORE_SECRET'],
                        public_ip=os.environ['BORE_PUBLIC_IP'],
                    )
                )
            case 'ip':
                # return (
                #     socket.gethostbyname(socket.getfqdn())
                #     if sys.platform == 'linux' else
                #     socket.gethostbyname(socket.gethostname())
                # )
                rsp = run_cmd_line('ipconfig', shell=True)
                rsp = rsp[rsp.index('Wireless LAN adapter Wi-Fi'):]
                ip = re.search(r'IPv4 Address.+: ([.\d]+)', rsp).group(1)
                return ip
            case 'likianta':
                return 'C:/Likianta'
            case 'por':
                return 'poetry run'
            case 'pox':
                return 'poetry run python'
            case 'py':
                return 'python'
            case 'python':
                return 'python'
            case 'strun':
                return (
                    'python -m poetry run streamlit run '
                    '--browser.gatherUsageStats false '
                    '--runner.magicEnabled false '
                    '--server.headless true '
                    '--server.port'
                )
        raise Exception(m.group())
    
    return re.sub(r'<(\w+)>', _inplace, cmd)


if __name__ == '__main__':
    # $env.BORE_SECRET = '...'
    # $env.BORE_PUBLIC_IP = '...'
    # strun 2001 mypc_task_manager/app.py
    st.set_page_config('MyPC Task Manager', layout='wide')
    main()
