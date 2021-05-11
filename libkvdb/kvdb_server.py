from twisted.internet import reactor, protocol, endpoints, utils, defer
from twisted.protocols import basic

import glob

import kvdb

import logging

logging.basicConfig(level="INFO")


class Command:
    # extend
    def __init__(self, command_raw):
        self._command_raw = command_raw

    # extend
    def execute(self, factory):
        return factory.__getattribute__(self._op_name)

    @classmethod
    def parse(cls, command):
        resp = {True: None,
                command == "LIST": ListCommand,
                glob.fnmatch.fnmatch(command, "GET *"): GetCommand,
                glob.fnmatch.fnmatch(command, "PUT *"): PutCommand,
                glob.fnmatch.fnmatch(command, "DEL *"): DeleteCommand,
                glob.fnmatch.fnmatch(command, "LIST ONLY *"): ListPredicateCommand
                }[True]
        if not resp:
            raise NameError("No such command")
        return resp(command)


class GetCommand(Command):
    def __init__(self, command):
        super().__init__(command)
        self._op_name = "get_by_key"
        self._key = self._command_raw.split()[-1]
    
    def execute(self, factory):
        return super().execute(factory)(self._key)


class PutCommand(Command):
    def __init__(self, command):
        super().__init__(command)
        self._op_name = "put_key_value"
        self._key = self._command_raw.split()[-2]
        self._value = self._command_raw.split()[-1]

    
    def execute(self, factory):
        return super().execute(factory)(self._key, self._value)


class DeleteCommand(Command):
    def __init__(self, command):
        super().__init__(command)
        self._op_name = "delete_by_key"
        self._key = self._command_raw.split()[-1]
    
    def execute(self, factory):
        return super().execute(factory)(self._key)


class ListCommand(Command):
    def __init__(self, _command):
        super().__init__(None)
        self._op_name = "list_keys"
    
    def execute(self, factory):
        return super().execute(factory)()


class ListPredicateCommand(Command):
    def __init__(self, command):
        super().__init__(command)
        self._op_name = "list_keys"

        self._predicate = self._command_raw.split(" ")[-1]

    def execute(self, factory):
        return super().execute(factory)(self._predicate)



class KVDBProtocol(basic.LineReceiver):
    def lineReceived(self, command):
        command = command.decode()
        logging.info(f"Called with {command}")
        resp = Command.parse(command).execute(self.factory)

        def onError(err):
            logging.error(err)
            return b"Server error"

        resp.addErrback(onError)

        def writeResponse(resp):
            self.transport.write(f"{resp}".encode() + b"\r\n")
            self.transport.loseConnection()

        resp.addCallback(writeResponse)


class KVDBFactory(protocol.ServerFactory):
    protocol = KVDBProtocol

    def __init__(self, db_name):
        self._db_name = db_name
        self._db = kvdb.KVDB(self._db_name)

    def get_by_key(self, key):
        return defer.succeed(self._db.get(key))

    def put_key_value(self, key, value):
        return defer.succeed(self._db.put(key, value))

    def list_keys(self, glob_predicate=None):
        if glob_predicate:
            return defer.succeed(glob.fnmatch.filter(self._db.list_keys(), glob_predicate))
        return defer.succeed(self._db.list_keys())

    def delete_by_key(self, key):
        return defer.succeed(self._db.delete(key))
        # return utils.getProcessOutput(b"KVDB", [user])

if __name__ == "__main__":
    fingerEndpoint = endpoints.serverFromString(reactor, "tcp:2026") # 0x7ea = tea
    fingerEndpoint.listen(KVDBFactory("/tmp/kvdb"))

    logging.info("KVDB Server started")

    reactor.run()

