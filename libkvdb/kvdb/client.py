# from twisted.internet import reactor, protocol, endpoints, utils, defer
# from twisted.protocols import basic

# import glob
# import kvdb

import json, ast

import logging
import socket
import sys  


logging.basicConfig(level="INFO")


class KVDBClient:

    def __init__(self, host="localhost", port=2026):
        self._host = host
        self._port = port

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            sys.exit()

        self._socket.connect((self._host , self._port))

        self.cmds = {
            "GET":       "GET|{key}",
            "LIST":      "LIST",
            "LIST ONLY": "LIST ONLY|{key}",
            "DEL":       "DEL|{key}",
            "PUT":       "PUT|{key}|{value}"
        }

    def send(self, cmd, key=None, value=None):
        if cmd in self.cmds:
            request = self.cmds[cmd].format(key=key, value=value) + "\r\n"
            try:
                self._socket.sendall(request.encode())
            except socket.error:
                sys.exit()

            reply_size = self._socket.recv(6)
            reply = self._socket.recv(int(reply_size)).decode()
            __trailer = self._socket.recv(2) # because of \r\n

            return ast.literal_eval(reply) if reply.startswith("[") or reply.endswith("]") else reply
        else:
            raise KeyError(f"No such command. Available commands are: {self.cmds}")

    def get(self, key):
        return self.send("GET", key)
    
    def put(self, key, value):
        return self.send("PUT", key, value)

    def delete(self, key):
        return self.send("DEL", key)
    
    def list_keys(self):
        return self.send("LIST")

    def list_only(self, predicate):
        return self.send("LIST ONLY", predicate)


