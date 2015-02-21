# Copyright 2015 DaoCloud Inc. All Rights Reserved.

import unittest
from hamcrest import *  # noqa
from nose.tools import raises

from server.command.command import Command, State
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

    def test_queue_cmd_state(self):
        queue = MemoryCommandQueue()

        queue.add_command('runtime-1', Command('test'))
        queue.add_command('runtime-1', Command('test'))

        commands = queue.get_queued_commands('runtime-1')
        assert_that(commands, has_length(2))

        for cmd in queue._peek_queue('runtime-1'):
            assert_that(cmd.state(), is_(State.STARTED))

        commands = queue.get_queued_commands('runtime-1')
        assert_that(commands, has_length(0))

    def test_set_result(self):
        queue = MemoryCommandQueue()

        queue.add_command('runtime-1', Command('test'))  # seq_id: 1
        queue.add_command('runtime-1', Command('test'))  # seq_id: 2

        queue.set_command_result('runtime-1', 1, True, 100)

        commands = queue.get_queued_commands('runtime-1')
        assert_that(commands, has_length(1))

        command = queue._get_command('runtime-1', 1)
        assert_that(command.state(), is_(State.DONE))
        assert_that(command.result, is_(100))

    @raises(RuntimeNotFound)
    def test_set_result_no_runtime(self):
        queue = MemoryCommandQueue()
        command = Command('test')
        queue.add_command('runtime-1', command)
        queue.set_command_result('runtime-2', 1, True, 100)

    @raises(CommandNotInQueue)
    def test_set_result_no_command(self):
        queue = MemoryCommandQueue()
        queue.add_command('runtime-1', Command('test'))
        queue.set_command_result('runtime-1', 2, True, 100)
