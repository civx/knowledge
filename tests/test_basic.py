import unittest
from nose.tools import eq_
import os

from sqlalchemy import create_engine

from knowledge.model import init_model, metadata, Entity, setup_knowledge


class TestBasics(unittest.TestCase):
    def setUp(self):
        self.session = setup_knowledge('sqlite:///:memory:')

    def test_basic_one(self):
        """ Basic usage. """
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        eq_(apple.name, 'apple')

    def test_associating_facts_unicode_by_key(self):
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        apple['foo'] = u'bar'
        eq_(apple['foo'], 'bar')

    def test_associating_facts_unicode_by_attr(self):
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        apple['foo'] = u'bar'
        eq_(apple.foo, 'bar')

    def test_associating_facts_unicode_by_get(self):
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('foo'), 'bar')

    def test_associating_facts_get_default(self):
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('baz'), None)

    def test_associating_facts_get_custom_default(self):
        apple = Entity('apple')
        self.session.add(apple)
        self.session.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('baz', 'zomg'), 'zomg')
