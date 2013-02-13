import unittest
from nose.tools import eq_
import os

from knowledge.model import Entity

# TODO -- make this an in-memory database, not in /tmp
filename = '/tmp/testing-knowledge-db.db'

class TestBasics(unittest.TestCase):
    def test_basic_one(self):
        """ Basic usage. """
        apple = Entity('apple')
        eq_(apple.name, 'apple')

    def test_associating_facts_unicode_by_key(self):
        apple = Entity('apple')
        apple['foo'] = u'bar'
        eq_(apple['foo'], u'bar')

    def test_associating_facts_unicode_by_attr(self):
        apple = Entity('apple')
        apple['foo'] = u'bar'
        eq_(apple.foo, 'bar')

if __name__ == '__main__':
    unittest.main()
