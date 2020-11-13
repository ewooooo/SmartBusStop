from psutil import process_iter
from signal import SIGTERM # or SIGKILL

def kill_port():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 12345:
                proc.send_signal(SIGTERM) # or SIGKILL
                continue

if __name__ == "__main__":
    kill_port()