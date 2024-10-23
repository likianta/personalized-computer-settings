from collections import defaultdict

import lk_logger
import psutil
import win32con
import win32gui
import win32process

lk_logger.setup(quiet=True)
print(':tvi2', 'reloaded')


def _enumerate_windows() -> dict[str, dict]:
    def _enum(hwnd, data_collector: dict[str, dict]):
        if win32gui.IsWindowVisible(hwnd):
            if title := win32gui.GetWindowText(hwnd):
                tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc_name = _get_proc_name_by_pid(pid).lower()
                data_collector[proc_name][title] = (hwnd, pid, tid)
    
    def _get_proc_name_by_pid(pid: int) -> str:
        return psutil.Process(pid).name()
    
    data_collector = defaultdict(dict)
    win32gui.EnumWindows(_enum, data_collector)
    
    print(data_collector, ':l')
    return data_collector


windows = _enumerate_windows()


# -----------------------------------------------------------------------------

def maximize_windows(proc_name: str) -> None:
    for k, v in windows[proc_name].items():
        hwnd = v[0]
        win32gui.ShowWindow(
            hwnd, win32con.SW_MAXIMIZE
        )


def refresh_windows() -> None:
    global windows
    windows = _enumerate_windows()

# por ipython -i mypc_settings/windows_layout_manager.py
