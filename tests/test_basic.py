import unittest
from nose.tools import eq_
import os

from sqlalchemy import create_engine
from knowledge.model import setup_knowledge, Entity
from knowledge.model import DBSession

# TODO -- make this an in-memory database, not in /tmp
filename = '/tmp/testing-knowledge-db.db'

class TestBasics(unittest.TestCase):
    def setUp(self):
        uri = "sqlite:///%s" % filename
        setup_knowledge(uri)
        #engine = create_engine('sqlite:///knowledge.db')
        #init_model(engine)
        #metadata.create_all(engine)

    def tearDown(self):
        os.remove(filename)

    def test_basic_one(self):
        """ Basic usage. """
        apple = Entity('apple')
        eq_(apple.name, 'apple')

    def test_basic_two(self):
        apple = Entity('apple')
        eq_(apple.name, 'apple')
        DBSession.commit()
        # Did we survive?

    def test_associating_facts_unicode_by_key(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple['foo'], u'bar')

    def test_associating_facts_unicode_by_attr(self):
        apple = Entity('apple')
        DBSession.add(apple)
        DBSession.commit()
        apple['foo'] = u'bar'
        eq_(apple.foo, 'bar')

if __name__ == '__main__':
    unittest.main()
