# Copyright 2015 DaoCloud Inc. All Rights Reserved.
import json
import time
import unittest

from hamcrest import *  # noqa

from server.command.command import Command, State, CommandEncoder
from server.command.echo_command import EchoCommand


class TestCommand(unittest.TestCase):

    def test_command_state(self):
        command = Command('command-1')
        assert_that(command.state(), is_(State.QUEUED))
        command.start()
        assert_that(command.state(), is_(State.STARTED))
        command.done()
        assert_that(command.state(), is_(State.DONE))

    def test_command_fail(self):
        command = Command('command-1')
        assert_that(command.state(), is_(State.QUEUED))
        command.fail()
        assert_that(command.state(), is_(State.FAIL))

    def test_command_timeout(self):
        command = Command('command-1')
        assert_that(command.state(), is_(State.QUEUED))
        command._started_at = time.time() - 31
        assert_that(command.state(), is_(State.TIMEOUT))

    def test_command_finished(self):
        command = Command('command-1')
        assert_that(command.is_finished(), is_(False))
        command.start()
        assert_that(command.is_finished(), is_(False))
        command.done()
        assert_that(command.is_finished(), is_(True))

    def test_command_result(self):
        command = Command('command-1')
        assert_that(command.state(), is_(State.QUEUED))
        command.start()
        assert_that(command.state(), is_(State.STARTED))
        command.done(12)
        assert_that(command.state(), is_(State.DONE))
        assert_that(command.result, is_(12))

    def test_command_fail_result(self):
        command = Command('command-1')
        assert_that(command.state(), is_(State.QUEUED))
        command.start()
        assert_that(command.state(), is_(State.STARTED))
        command.fail('failed')
        assert_that(command.state(), is_(State.FAIL))
        assert_that(command.result, is_('failed'))

    def test_command_dict(self):
        command = Command('command-1')
        result = command.to_dict()
        assert_that(result['name'], command.name)
        assert_that(result['seq_id'], command.seq_id)
        assert_that(len(result), is_(2))

    def test_echo_command_dict(self):
        command = EchoCommand('hello')
        result = command.to_dict()
        assert_that(result['name'], 'echo')
        assert_that(result['seq_id'], command.seq_id)
        assert_that(result['message'], command.message)
        assert_that(len(result), is_(3))

    def test_command_json(self):
        command = Command('command-1')
        result = json.loads(json.dumps(command, cls=CommandEncoder))
        assert_that(result['name'], command.name)
        assert_that(result['seq_id'], command.seq_id)
        assert_that(len(result), is_(2))

    def test_echo_command_json(self):
        command = EchoCommand('hello')
        result = json.loads(json.dumps(command, cls=CommandEncoder))
        assert_that(result['name'], 'echo')
        assert_that(result['seq_id'], command.seq_id)
        assert_that(result['message'], command.message)
        assert_that(len(result), is_(3))

    def test_command_list_json(self):
        command = EchoCommand('hello')
        result = json.loads(json.dumps([command], cls=CommandEncoder))
        assert_that(result, has_length(1))
        assert_that(result[0]['name'], 'echo')
        assert_that(result[0]['seq_id'], command.seq_id)
        assert_that(result[0]['message'], command.message)
        assert_that(len(result[0]), is_(3))
