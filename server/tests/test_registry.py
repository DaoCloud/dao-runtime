import unittest
from hamcrest import *  # noqa

import server.registry as registry


class TestRegistery(unittest.TestCase):

    def setUp(self):
        registry.clear()

    def test_register_unregister(self):
        registry.register(registry.Runtime('runtime-1'))
        assert_that(registry.size(), is_(1))
        registry.register(registry.Runtime('runtime-2'))
        assert_that(registry.size(), is_(2))

        registry.unregister('runtime-1')
        assert_that(registry.size(), is_(1))
        registry.unregister('runtime-2')
        assert_that(registry.size(), is_(0))

    def test_unregister_no_existed(self):
        registry.register(registry.Runtime('runtime-1'))
        assert_that(registry.size(), is_(1))

        registry.unregister('not-existed')
        assert_that(registry.size(), is_(1))

    def test_is_registered(self):
        assert_that(registry.is_registered('runtime-1'), is_(False))
        registry.register(registry.Runtime('runtime-1'))
        assert_that(registry.is_registered('runtime-1'), is_(True))
