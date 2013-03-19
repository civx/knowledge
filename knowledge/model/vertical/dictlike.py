"""Mapping a vertical table as a dictionary.

This example illustrates accessing and modifying a "vertical" (or
"properties", or pivoted) table via a dict-like interface.  These are tables
that store free-form object properties as rows instead of columns.  For
example, instead of::

  # A regular ("horizontal") table has columns for 'species' and 'size'
  Table('animal', metadata,
        Column('id', Integer, primary_key=True),
        Column('species', Unicode),
        Column('size', Unicode))

A vertical table models this as two tables: one table for the base or parent
entity, and another related table holding key/value pairs::

  Table('animal', metadata,
        Column('id', Integer, primary_key=True))

  # The properties table will have one row for a 'species' value, and
  # another row for the 'size' value.
  Table('properties', metadata
        Column('animal_id', Integer, ForeignKey('animal.id'),
               primary_key=True),
        Column('key', UnicodeText),
        Column('value', UnicodeText))

Because the key/value pairs in a vertical scheme are not fixed in advance,
accessing them like a Python dict can be very convenient.  The example below
can be used with many common vertical schemas as-is or with minor adaptations.
"""

class VerticalProperty(object):
    """A key/value pair.

    This class models rows in the vertical table.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<%s %r=%r>' % (self.__class__.__name__, self.key, self.value)


class VerticalPropertyDictMixin(object):
    """Adds obj[key] access to a mapped class.

    This is a mixin class.  It can be inherited from directly, or included
    with multiple inheritence.

    Classes using this mixin must define two class properties::

    _property_type:
      The mapped type of the vertical key/value pair instances.  Will be
      invoked with two positional arugments: key, value

    _property_mapping:
      A string, the name of the Python attribute holding a dict-based
      relation of _property_type instances.

    Using the VerticalProperty class above as an example,::

      class MyObj(VerticalPropertyDictMixin):
          _property_type = VerticalProperty
          _property_mapping = 'props'

      mapper(MyObj, sometable, properties={
        'props': relation(VerticalProperty,
                          collection_class=attribute_mapped_collection('key'))})

    Dict-like access to MyObj is proxied through to the 'props' relation::

      myobj['key'] = 'value'
      # ...is shorthand for:
      myobj.props['key'] = VerticalProperty('key', 'value')

      myobj['key'] = 'updated value']
      # ...is shorthand for:
      myobj.props['key'].value = 'updated value'

      print myobj['key']
      # ...is shorthand for:
      print myobj.props['key'].value

    """

    _property_type = VerticalProperty
    _property_mapping = None

    __map = property(lambda self: getattr(self, self._property_mapping))

    def __getitem__(self, key):
        return self.__map[key].value

    def __getattr__(self, key):
        return self.__map[key].value

    def get(self, key, default=None):
        value = self.__map.get(key, default)
        if hasattr(value, 'value'):
             return value.value
        return value

    def __setitem__(self, key, value):
        property = self.__map.get(key, None)
        if property is None:
            self.__map[key] = self._property_type(key, value)
        else:
            property.value = value

    def __delitem__(self, key):
        del self.__map[key]

    def __delattr__(self, key):
        del self.__map[key]

    def __contains__(self, key):
        return key in self.__map

    # Implement other dict methods to taste.  Here are some examples:
    def keys(self):
        return self.__map.keys()

    def values(self):
        return [prop.value for prop in self.__map.values()]

    def items(self):
        return [(key, prop.value) for key, prop in self.__map.items()]

    def __iter__(self):
        return iter(self.keys())
