# TODO(pyu): Implement real command
# TODO(pyu): Implement marshal/unmarshal command

import enum
import time

from server.command.seq_generator import next_seq_id


@enum.unique
class State(enum.Enum):
    DONE = 0
    QUEUED = 1
    STARTED = 2
    FAIL = 3
    TIMEOUT = 4


class BaseCommand(object):

    DEFAULT_TIMEOUT = 30

    def __init__(self, name, seq_id):
        self.name = name
        self.seq_id = seq_id
        self._state = State.QUEUED
        self._started_at = time.time()

    def state(self):
        if not self.is_finished() and \
           time.time() - self._started_at > self.DEFAULT_TIMEOUT:
            self._state = State.TIMEOUT

        return self._state

    def is_finished(self):
        return self._state == State.FAIL or self._state == State.DONE or \
            self._state == State.TIMEOUT

    def is_queued(self):
        return self._state == State.QUEUED

    def start(self):
        self._state = State.STARTED

    # TODO(pyu): reason
    def fail(self):
        self._state = State.FAIL

    # TODO(pyu): result
    def done(self):
        self._state = State.DONE

    def __repr__(self):
        return "<Command seq_id: %d, name: %s, state: %s>" % \
               (self.seq_id, self.name, self._state)


class Command(BaseCommand):

    def __init__(self, name):
        super(Command, self).__init__(name, next_seq_id())

    def __repr__(self):
        return super(Command, self).__repr__()
