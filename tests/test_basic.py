import unittest
from nose.tools import eq_
import os

from sqlalchemy import create_engine

from knowledge.model import init_model, metadata, DBSession, Entity


class TestBasics(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        init_model(engine)
        metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()

    def test_basic_one(self):
        """ Basic usage. """
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        eq_(apple.name, 'apple')

    def test_associating_facts_unicode_by_key(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple['foo'], 'bar')

    def test_associating_facts_unicode_by_attr(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple.foo, 'bar')

    def test_associating_facts_unicode_by_get(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('foo'), 'bar')

    def test_associating_facts_get_default(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('baz'), None)

    def test_associating_facts_get_custom_default(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple.get('baz', 'zomg'), 'zomg')
