import multiprocessing
import threading

import aes
import time
import sys

from queue import Queue, Empty

CHUNK_SIZE = 1024 ** 3
INPUT_FILE = 'random.bin'
key = b'0123456789abcdef'


def worker(queue):
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


def benchmark(n_threads=0):
    if n_threads == 0:
        n_threads = multiprocessing.cpu_count()

    queue = Queue()
    threads = []
    for i in range(n_threads):
        threads.append(threading.Thread(target=worker, args=(queue,)))
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
