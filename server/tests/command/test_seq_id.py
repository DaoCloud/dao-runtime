import sys
import unittest

from hamcrest import *  # noqa

from server.command.seq_generator import _set_seq_id, next_seq_id


class TestSeqGenerator(unittest.TestCase):

    def setUp(self):
        _set_seq_id(0)

    def tearDown(self):
        _set_seq_id(0)

    def test_seq_id(self):
        assert_that(next_seq_id(), is_(1))
        assert_that(next_seq_id(), is_(2))

    def test_seq_id_overflow(self):
        _set_seq_id(sys.maxint)
        assert_that(next_seq_id(), is_(sys.maxint+1))
