import threading
import time

My_Lock = threading.Lock()

def worker(thread_name):
    with My_Lock:
        for val in range(20):
            print(f"{thread_name}: {val}")

thread_bar = threading.Thread(target=worker, args=("bar", ))
thread_foo = threading.Thread(target=worker, args=("foo", ))
thread_pos = threading.Thread(target=worker, args=("pos", ))

thread_bar.start()
thread_foo.start()
thread_pos.start()