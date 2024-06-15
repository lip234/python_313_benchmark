def test_hashlib():
    import hashlib
    s = b"0123456789abcdef"
    assert hashlib.md5(s).hexdigest() == '4032af8d61035123906e58e067140cc5'
    assert hashlib.sha1(s).hexdigest() == 'fe5567e8d769550852182cdf69d74bb16dff8e29'
    assert hashlib.sha224(s).hexdigest() == '7330215f6741fd2bacbd3658681a70f65e2e90a02887989018974ce8'
    assert hashlib.sha256(s).hexdigest() == '9f9f5111f7b27a781f1f1ddde5ebc2dd2b796bfc7365c9c28b548e564176929f'
    assert hashlib.sha384(
        s).hexdigest() == 'fc6304023487cb6f85ac80e47817760c6b153c02da46c6429649e963b031e525deb160e3da5b645fa843fab2f25b913f'
    assert hashlib.sha3_224(s).hexdigest() == 'bbb7d56cc80a8c80e907f7d9240edc0be264aa173266b30918bc1065'
    assert hashlib.sha3_256(s).hexdigest() == 'a5df4caae9fdb5dbacf667075b709a2f30a115c43168af332062b42d4b0da01f'
    assert hashlib.sha3_384(
        s).hexdigest() == '56f351f754c418892eab4009e5f85c8d5436a591014503563e9395b8955264130e43758d01bd153e0a29e4e099a67998'
    assert hashlib.sha3_512(
        s).hexdigest() == '59d06155d25dffdb982729de8dce9d7855ca094d8bab8124b347c40668477056b3c27ccb7d71b54043d207ccd187642bf9c8466f9a8d0dbefb4c41633a7e39ef'
    assert hashlib.shake_128(s).hexdigest(20) == '0140c2303cbe77aa153de760b821de1833418685'
    assert hashlib.shake_256(s).hexdigest(
        40) == 'f205e448f13f75e242c237ac0c1505b0020cde5b8bd5e6f0b05c444299817ff7906cbdc8eb9a28bd'


def test_sqlite3():
    import sqlite3
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE test (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT)')
    conn.execute('INSERT INTO test (value) VALUES (?)', ('test1',))
    conn.execute('INSERT INTO test (value) VALUES (?)', ('test2',))
    conn.execute('INSERT INTO test (value) VALUES (?)', ('test3',))
    conn.execute('INSERT INTO test (value) VALUES (?)', ('test4',))
    conn.execute('INSERT INTO test (value) VALUES (?)', ('test5',))
    conn.commit()

    cur = conn.execute('SELECT * FROM test')
    data = cur.fetchall()
    conn.close()
    assert len(data) == 5


def test_marshal():
    import marshal
    serialised_int = marshal.dumps(1024 ** 3)
    deserialised_int = marshal.loads(serialised_int)
    assert type(deserialised_int) is int and deserialised_int == 1024 ** 3

    s = 'this is a magic string!'
    serialised_str = marshal.dumps(s)
    deserialised_str = marshal.loads(serialised_str)
    assert type(deserialised_str) is str and deserialised_str == s


def test_urllib():
    from urllib.request import urlopen
    with urlopen('http://google.com/generate_204') as resp:
        assert resp.code == 204


def test_ctypes():
    import ctypes

    libc = ctypes.CDLL('libc.so.6')
    libc.sprintf.argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_char_p, ctypes.c_char_p]
    libc.sprintf.restype = ctypes.c_int

    buffer = ctypes.create_string_buffer(32)
    ret = libc.sprintf(buffer, b"Hello %s!", b'World')
    assert ret == 12
    assert buffer.value == b'Hello World!'


if __name__ == '__main__':
    test_hashlib()
    test_sqlite3()
    test_marshal()
    test_urllib()
    test_ctypes()
