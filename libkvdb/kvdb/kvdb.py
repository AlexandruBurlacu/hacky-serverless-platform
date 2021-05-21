from pathlib import Path

from hashlib import sha1

import pickle

import logging

from threading import Lock
import bisect

#-------

def serialize(value):
    return pickle.dumps(value, protocol=pickle.DEFAULT_PROTOCOL)

def deserialize(value):
    return pickle.loads(value)

#-------

def get_hashstr(key):
    return sha1(f"{key}".encode()).hexdigest()


class KVDB:
    def __init__(self, path: str):
        self.db_path = Path(path)
        self.db_path.mkdir(exist_ok=True)

        self.index = self.db_path / Path("keys.index")
        self.index.touch()

    def put(self, key, value):
        with Lock():
            hashed_key = get_hashstr(key)
            subdir = self.db_path / Path(hashed_key[:2])
            subdir.mkdir(exist_ok=True)

            value_file = subdir / Path(hashed_key[2:])
            value_file.write_bytes(serialize(value))

            data = self.index.read_text().splitlines()
            if key not in data:
                bisect.insort(data, key)
            self.index.write_text("\n".join(data))


    def get(self, key):
        hashed_key = get_hashstr(key)
        value = self.db_path / Path(hashed_key[:2]) / Path(hashed_key[2:])
        return deserialize(value.read_bytes())

    def list_keys(self):
        return self.index.read_text().splitlines()

    def delete(self, key):
        with Lock():
            hashed_key = get_hashstr(key)
            value = self.db_path / Path(hashed_key[:2]) / Path(hashed_key[2:])
            value.unlink()

            index = self.index.read_text().splitlines()
            index.remove(key)
            self.index.write_text("\n".join(index))
