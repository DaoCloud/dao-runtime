import time
import unittest

from hamcrest import *  # noqa

from server.command.command import Command, State


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
