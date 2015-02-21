import threading

from server.queue.queue import CommandQueue, RuntimeNotFound, CommandNotInQueue


class MemoryCommandQueue(CommandQueue):
    """ In memory command queue. Not an optimal solution.
    """

    def __init__(self):
        self._queue = {}
        self._lock = threading.Lock()

    def add_command(self, runtime_name, command):
        with self._lock:
            if runtime_name not in self._queue:
                self._queue[runtime_name] = []
            self._queue[runtime_name].append(command)

    def get_queued_commands(self, runtime_name, seq_id=0):
        with self._lock:
            cmds = self._peek_queue(runtime_name, seq_id)

            for cmd in cmds:
                cmd.start()

            return cmds

    def set_command_result(self, runtime_name, command):
        with self._lock:
            if runtime_name not in self._queue:
                raise RuntimeNotFound("Runtime not found")

            indexes = [i for i, cmd in enumerate(self._queue[runtime_name])
                       if cmd.seq_id == command.seq_id]
            if not indexes:
                raise CommandNotInQueue("Command not found in queue")

            # Only one command with specific req_id
            assert len(indexes) == 1

            index = indexes[0]
            self._queue[runtime_name][index] = command

    def _peek_queue(self, runtime_name, seq_id=0):
        if runtime_name not in self._queue:
            return []
        return [cmd for cmd in self._queue[runtime_name]
                if cmd.seq_id > seq_id and cmd.is_queued()]

    # For unit test
    def _clear(self):
        self._queue = {}


queue = MemoryCommandQueue()
