
import json
from hamcrest import *  # noqa
import unittest

from server.command.echo_command import EchoCommand
from server.queue.in_memory_queue import queue
import server.registry as registry
from server.web.api import api
import server.web.v1  # noqa


class TestApiV1(unittest.TestCase):

    def setUp(self):
        self.app = api.test_client()
        registry.clear()
        queue._clear()

    def test_register_unregister(self):
        result = self.app.post('/api/v1/runtimes',
                               headers={'Content-Type': 'application/json'},
                               data='{"name":"sample"}')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_(''))
        assert_that(registry.size(), is_(1))
        assert_that(registry.is_registered('sample'), is_(True))

        result = self.app.delete('/api/v1/runtimes/sample')
        assert_that(result.status_code, is_(200))
        assert_that(registry.size(), is_(0))
        assert_that(registry.is_registered('sample'), is_(False))

    def test_invalid_register(self):
        # Body not json
        result = self.app.post('/api/v1/runtimes',
                               headers={'Content-Type': 'application/json'},
                               data='not_json')
        assert_that(result.status_code, is_(400))

        # No Content-Type
        result = self.app.post('/api/v1/runtimes',
                               data='not_json')
        assert_that(result.status_code, is_(400))

        # Missing field
        result = self.app.post('/api/v1/runtimes',
                               headers={'Content-Type': 'application/json'},
                               data='{"l_name": "Turing","f_name": "Alan"}')
        assert_that(result.status_code, is_(400))

    def test_polling(self):
        # Start empty queue, polling returns empty list
        result = self.app.get('/api/v1/runtimes/sample/requests')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('[]'))

        # Add 2 commands in queue, and polling returns 2 commands
        queue.add_command('sample', EchoCommand('test-1'))  # seq_id: 1
        queue.add_command('sample', EchoCommand('test-2'))  # seq_id: 2

        result = self.app.get('/api/v1/runtimes/sample/requests')
        assert_that(result.status_code, is_(200))
        data = json.loads(result.data)
        assert_that(data, has_length(2))
        assert_that(data[0]['seq_id'], is_(1))
        assert_that(data[0]['name'], is_('echo'))
        assert_that(data[0]['message'], is_('test-1'))
        assert_that(data[1]['seq_id'], is_(2))
        assert_that(data[1]['name'], is_('echo'))
        assert_that(data[1]['message'], is_('test-2'))

        # polling again, returns empty list
        result = self.app.get('/api/v1/runtimes/sample/requests')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('[]'))

        # Add 2 commands in queue again, and polling
        queue.add_command('sample', EchoCommand('test-3'))  # seq_id: 3
        queue.add_command('sample', EchoCommand('test-4'))  # seq_id: 4

        # Polling from seq_id 3 this time
        result = self.app.get('/api/v1/runtimes/sample/requests?seq_id=3')
        assert_that(result.status_code, is_(200))
        data = json.loads(result.data)
        assert_that(data, has_length(1))

    def test_callback(self):
        result = self.app.post('/api/v1/runtimes/sample/callback')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('callback sample'))

if __name__ == '__main__':
    unittest.main()
