
import enum
import time

from json import JSONEncoder

from server.command.seq_generator import next_seq_id


@enum.unique
class State(enum.Enum):
    DONE = 0
    QUEUED = 1
    STARTED = 2
    FAIL = 3
    TIMEOUT = 4


class BaseCommand(object):

    # Number of seconds. If not hearing the command back for this amount of
    # time, set the command state as TIMEOUT.
    DEFAULT_TIMEOUT = 30

    # Filtered fields from dict/json, besides fields starting with _
    HIDDEN_FIELDS = ['result']

    def __init__(self, name, seq_id):
        self.name = name
        self.seq_id = seq_id
        self.result = None
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

    def fail(self, result=None):
        self.result = result
        self._state = State.FAIL

    def done(self, result=None):
        self.result = result
        self._state = State.DONE

    def __repr__(self):
        return "<Command seq_id: %d, name: %s, state: %s>" % \
               (self.seq_id, self.name, self._state)

    def to_dict(self):
        """ dict representation of command. It filters out HIDDEN_FIELDS and
        fields starting with _ .
        """
        return dict(
                   (k, v) for k, v in self.__dict__.items()
                   if k not in self.HIDDEN_FIELDS and not k.startswith('_')
               )


class Command(BaseCommand):

    def __init__(self, name):
        super(Command, self).__init__(name, next_seq_id())


class CommandEncoder(JSONEncoder):
    """ Json encoder for Command
    """

    def default(self, o):
        if isinstance(o, Command):
            return o.to_dict()
        else:
            super(CommandEncoder, self).default(o)
