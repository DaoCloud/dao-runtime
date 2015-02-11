
from hamcrest import *  # noqa
import unittest

from server.web.api import api
import server.web.v1  # noqa
import server.registry as registry


class TestApiV1(unittest.TestCase):

    def setUp(self):
        self.app = api.test_client()
        registry.clear()

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
        result = self.app.get('/api/v1/runtimes/sample/requests')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('polling sample'))

    def test_callback(self):
        result = self.app.post('/api/v1/runtimes/sample/callback')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('callback sample'))

if __name__ == '__main__':
    unittest.main()
