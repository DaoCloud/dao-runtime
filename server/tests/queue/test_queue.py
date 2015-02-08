
import unittest
from hamcrest import *  # noqa
from nose.tools import raises

from server.command.command import Command
from server.command.seq_generator import _set_seq_id
from server.queue.in_memory_queue import MemoryCommandQueue
from server.queue.queue import RuntimeNotFound, CommandNotInQueue


class TestCommandQueue(unittest.TestCase):

    def setUp(self):
        _set_seq_id(0)

    def tearDown(self):
        _set_seq_id(0)

    def test_queue(self):
        queue = MemoryCommandQueue()

        queue.add_command('runtime-1', Command('test'))
        queue.add_command('runtime-1', Command('test'))

        commands = queue.get_queued_commands('runtime-1')
        assert_that(commands, has_length(2))
        commands = queue.get_queued_commands('runtime-2')
        assert_that(commands, has_length(0))
        commands = queue.get_queued_commands('runtime-1', 2)
        assert_that(commands, has_length(0))

    def test_set_result(self):
        queue = MemoryCommandQueue()

        command = Command('test')
        queue.add_command('runtime-1', command)
        queue.add_command('runtime-1', Command('test'))

        command.fail()
        queue.set_command_result('runtime-1', command)

        commands = queue.get_queued_commands('runtime-1')
        assert_that(commands, has_length(1))

    @raises(RuntimeNotFound)
    def test_set_result_no_runtime(self):
        queue = MemoryCommandQueue()
        command = Command('test')
        queue.add_command('runtime-1', command)
        queue.set_command_result('runtime-2', command)

    @raises(CommandNotInQueue)
    def test_set_result_no_command(self):
        queue = MemoryCommandQueue()
        queue.add_command('runtime-1', Command('test'))
        queue.set_command_result('runtime-1', Command('test'))
