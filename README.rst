KnowledgeDB
-----------

Knowledge is a polymorphic vertical database based on SQLAlchemy.  It provides
a dict-like interface to the database.

Knowledge is comprised of two related objects: Fact()s and Entity()s.  Entities
can be created and then have arbitrary facts applied to them.  Before Knowledge
can be used, the DB has to be set up with SQLAlchemy as follows::

    from sqlalchemy import create_engine
    from knowledge.model import init_model, metadata
    engine = create_engine('sqlite:///knowledge.db')
    init_model(engine)
    metadata.create_all(engine)

Using knowledge is easy.  Entities are created with a key, then facts about
the entity can be applied like values in a dictionary::

    from knowledge.model import Entity, DBSession

    monster = Entity(u'Monster')
    fairy = Entity(u'Fairy')
    rjbean = Entity(u'rjbean')
    monster[u'color'] = u'Green'
    monster[u'name'] = u'Lotharrr'
    fairy[u'flies'] = True
    fairy[u'name'] = u'Bell'
    rjbean[u'name'] = u'ralph'
    rjbean[u'flies'] = False
    rjbean[u'hacks'] = True

    DBSession.add(monster)
    DBSession.add(fairy)
    DBSession.add(rjbean)
    DBSession.commit()

Retrieving Entities and Facts from the DB works just like any other SQLAlchemy
application::

    from knowledge.model import Entity, DBSession

    # Query all the Entities out of knowledge
    knowledge_query = DBSession.query(Entity).all()
    for entity in knowledge_query:
        print entity, entity.facts.values()
