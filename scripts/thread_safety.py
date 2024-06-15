# Certain operations on Python's built-in types are atomic and are therefore thread-safe guaranteed by the GIL,
# such operations include `pop, `pop`, and `extend` on lists and operations.
# This script is to test if these operations are still thread-safe without the GIL.

import threading


def pop_worker(a_list):
    for _ in range(20000):
        a_list.pop(0)


def push_worker(a_list):
    for i in range(20000):
        a_list.append(i)


def main():
    a_list = []
    for i in range(100000):
        a_list.append(i)
    threads = [threading.Thread(target=pop_worker, args=(a_list,)),
               threading.Thread(target=push_worker, args=(a_list,)),
               threading.Thread(target=pop_worker, args=(a_list,)),
               threading.Thread(target=push_worker, args=(a_list,)),
               ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert len(a_list) == 100000


if __name__ == '__main__':
    main()
