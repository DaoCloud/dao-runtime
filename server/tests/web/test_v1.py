
import unittest
from server.web.server import api
import server.web.v1  # noqa

from hamcrest import *  # noqa


class TestApiV1(unittest.TestCase):

    def setUp(self):
        self.app = api.test_client()

    def test_register(self):
        result = self.app.post('/api/v1/runtimes')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_(''))

    def test_unregister(self):
        result = self.app.delete('/api/v1/runtimes/sample')
        assert_that(result.status_code, is_(200))
        assert_that(result.data, is_('unregister sample'))

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
