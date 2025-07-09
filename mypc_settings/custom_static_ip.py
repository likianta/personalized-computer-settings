import netifaces
import socket
from argsense import cli


@cli
def main() -> None:
    addr = _get_my_ip_address()
    info = _get_network_info(addr)
    print(info, ':v2l')
    
    a, b, c, d = info['gateway'].split('.')
    print('suggested ip range: [blue]{} ~ {}[/]'.format(
        '{}.{}.{}.{}'.format(a, b, c, '100'),
        '{}.{}.{}.{}'.format(a, b, c, '255'),
    ), ':r')


@cli
def dns_settings() -> None:
    """
    ref: https://www.powoke.com/article/post/8731.html
    """
    print(
        '''
        **suggested DNS settings:**
        
        | server     | address         |
        | ---------- | --------------- |
        | aliyun     | 223.5.5.5       |
        | aliyun     | 223.6.6.6       |
        | 114        | 114.114.114.114 |
        | 114        | 114.114.115.115 |
        | baidu      | 180.76.76.76    |
        | google     | 8.8.8.8         |
        | google     | 8.8.4.4         |
        | cloudflare | 1.1.1.1         |
        | cloudflare | 1.0.0.1         |
        | opendns    | 208.67.222.222  |
        | opendns    | 208.67.220.220  |
        ''',
        ':r2'
    )


def _get_my_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    addr = s.getsockname()[0]
    s.close()
    return addr


def _get_network_info(target_ip_addr: str) -> dict:
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for ip in addrs[netifaces.AF_INET]:
                if ip['addr'] == target_ip_addr:
                    return {
                        'address': ip['addr'],
                        'netmask': ip['netmask'],
                        'gateway': netifaces.gateways()
                        ['default'][netifaces.AF_INET][0],
                    }
    raise Exception


if __name__ == '__main__':
    # main()
    cli.run()
