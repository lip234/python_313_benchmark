import multiprocessing
import threading
import time
import sys
import os

import aes

from queue import Queue, Empty
from ctypes import *
from ctypes import wintypes

CHUNK_SIZE = 1024 ** 3
INPUT_FILE = 'random.bin'
key = b'0123456789abcdef'

# get the cpu index on which the current thread is executing
# ref: https://stackoverflow.com/questions/76166230/how-can-a-python-program-determine-which-core-it-is-running-on
if os.name == 'nt':
    def get_cpu_idx():
        class PROCESSOR_NUMBER(Structure):
            _fields_ = [("Group", wintypes.WORD),
                        ("Number", wintypes.BYTE),
                        ("Reserved", wintypes.BYTE)]

        pn = PROCESSOR_NUMBER()
        windll.kernel32.GetCurrentProcessorNumberEx(byref(pn))
        return pn.Number
else:
    def get_cpu_idx():
        libc = CDLL("libc.so.6")
        return libc.sched_getcpu()


def worker(queue, thread_idx, log_file, file_lock):
    cipher = aes.AES(key)
    while True:
        try:
            data = queue.get(block=False)
        except Empty:
            break
        # Pad the data
        if len(data) % 16 != 0:
            n = (16 - len(data) % 16)
            data += chr(n) * n
        for i in range(0, len(data), 16):
            plain_text = data[i:i + 16]
            cipher.encrypt_block(plain_text)
            with file_lock:
                print(thread_idx, get_cpu_idx(), file=log_file)


def benchmark(n_threads=0):
    if n_threads == 0:
        n_threads = multiprocessing.cpu_count()

    queue = Queue()
    threads = []
    file_lock = threading.Lock()
    log_file = open('aes_benchmark.log', 'a')
    for i in range(n_threads):
        threads.append(threading.Thread(target=worker, args=(queue, i, log_file, file_lock)))
    with open(INPUT_FILE, 'rb') as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            queue.put(chunk)
    [t.start() for t in threads]
    [t.join() for t in threads]


def main():
    n_threads = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    start_time = time.perf_counter()
    benchmark(n_threads)
    stop_time = time.perf_counter()
    print(f'Time taken: {stop_time - start_time}')


if __name__ == '__main__':
    main()
