import socket
import sys
import threading
import time


def parse(setup):
    settings = list()
    with open(setup) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) != 4:
                continue

            settings.append([(parts[0], int(parts[1])),
                             (parts[2], int(parts[3]))])
    return settings

def parse_args(args):
    assert len(args) == 4
    settings =[[(args[0], int(args[1])), (args[2], int(args[3]))], ]
    return settings


def server(address, address_dst):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind(address)
        dock_socket.listen(5)
        print('Forward {} -> {} succeed!'.format(address, address_dst))
        while True:
            socket_src, addr = dock_socket.accept()
            print('accept', addr)

            socket_dst = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_dst.connect(address_dst)

            stop_event = threading.Event()
            threading.Thread(target=forward, args=('forward', socket_src, socket_dst, stop_event)).start()
            threading.Thread(target=forward, args=('backword', socket_dst, socket_src, stop_event)).start()
    except Exception as e:
        print('service', address, '->', address_dst, 'stop:', repr(e))


def forward(direction, source, destination, stop_event):
    source.settimeout(10)
    destination.settimeout(10)
    message = ''
    while True:
        try:
            buf = source.recv(4096)
            # print(len(buf))

            if buf:
                destination.sendall(buf)
            else:
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)
                break
        except socket.timeout:
            if stop_event.is_set():
                message = 'Stop by peer thread'
                break
        except Exception as e:
            message = repr(e)
            break
    print(direction, 'stop:', message)
    stop_event.set()


if __name__ == '__main__':

    class Logger(object):
        def __init__(self, terminal, f):
            self.terminal = terminal
            self.file = f

        def write(self, message):
            self.terminal.write(message)
            self.file.write(message)
        
        def flush(self):
            self.terminal.flush()
            self.file.flush()
        
    f = open('log.txt', 'a')
    sys.stderr = Logger(sys.stderr, f)
    sys.stdout = Logger(sys.stdout, f)

    config_file = 'config'
    args = sys.argv[1:]

    settings = parse_args(args) if len(args) > 0 else parse(config_file)

    for setting in settings:
        t = threading.Thread(target=server, args=setting)
        t.start()

    # wait for <ctrl-c>
    while True:
        time.sleep(60)
