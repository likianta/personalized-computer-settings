import os
import lk_logger
from lk_utils import run_cmd_args

def update_user_environment(data: dict) -> None:
    for key, val in data.items():
        val = (
            ';'.join(val)
            .replace('/', '\\')
            .replace('http:\\\\', 'http://')
            .replace('https:\\\\', 'https://')
        )
        if os.environ.get(key) == val:
            print(key, val, ':v3s1')
        else:
            print(key, val, ':v4s1')
            with lk_logger.spinner(f'setting key: {key}'):
                run_cmd_args('setx', key, val)
