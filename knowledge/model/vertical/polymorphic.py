"""Mapping a polymorphic-valued vertical table as a dictionary.

This example illustrates accessing and modifying a "vertical" (or
"properties", or pivoted) table via a dict-like interface.  The 'dictlike.py'
example explains the basics of vertical tables and the general approach.  This
example adds a twist- the vertical table holds several "value" columns, one
for each type of data that can be stored.  For example::

  Table('properties', metadata
        Column('owner_id', Integer, ForeignKey('owner.id'),
               primary_key=True),
        Column('key', UnicodeText),
        Column('type_', Unicode(16)),
        Column('int_value', Integer),
        Column('char_value', UnicodeText),
        Column('bool_value', Boolean),
        Column('decimal_value', Numeric(10,2)))

For any given properties row, the value of the 'type_' column will point to the
'_value' column active for that row.

This example approach uses exactly the same dict mapping approach as the
'dictlike' example.  It only differs in the mapping for vertical rows.  Here,
we'll use a Python @property to build a smart '.value' attribute that wraps up
reading and writing those various '_value' columns and keeps the '.type_' up to
date.

Note: Something much like 'comparable_property' is slated for inclusion in a
      future version of SQLAlchemy.
"""

from sqlalchemy import *
from sqlalchemy.orm.interfaces import PropComparator, MapperProperty
from sqlalchemy.orm import session as sessionlib, comparable_property

# Using the VerticalPropertyDictMixin from the base example
from dictlike import VerticalPropertyDictMixin

class PolymorphicVerticalProperty(object):
    """A key/value pair with polymorphic value storage.

    Supplies a smart 'value' attribute that provides convenient read/write
    access to the row's current value without the caller needing to worry
    about the 'type_' attribute or multiple columns.

    The 'value' attribute can also be used for basic comparisons in queries,
    allowing the row's logical value to be compared without foreknowledge of
    which column it might be in.  This is not going to be a very efficient
    operation on the database side, but it is possible.  If you're mapping to
    an existing database and you have some rows with a value of str('1') and
    others of int(1), then this could be useful.

    Subclasses must provide a 'type_map' class attribute with the following
    form::

      type_map = {
         <python type> : ('type column value', 'column name'),
         # ...
      }

    For example,::

      type_map = {
        int: ('integer', 'integer_value'),
        str: ('varchar', 'varchar_value'),
      }

    Would indicate that a Python int value should be stored in the
    'integer_value' column and the .type_ set to 'integer'.  Conversely, if the
    value of '.type_' is 'integer, then the 'integer_value' column is consulted
    for the current value.
    """
    class Comparator(PropComparator):
        """A comparator for .value, builds a polymorphic comparison via CASE.

        Optional.  If desired, install it as a comparator in the mapping::

          mapper(..., properties={
            'value': comparable_property(PolymorphicVerticalProperty.Comparator,
                                         PolymorphicVerticalProperty.value)
          })
        """

        def _case(self):
            cls = self.prop.parent.class_
            whens = [(text("'%s'" % p[0]), getattr(cls, p[1]))
                     for p in cls.type_map.values()
                     if p[1] is not None]
            return case(whens, cls.type_, null())
        def __eq__(self, other):
            return cast(self._case(), String) == cast(other, String)
        def __ne__(self, other):
            return cast(self._case(), String) != cast(other, String)

    type_map = {
        type(None): (None, None),
        }

    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def _get_value(self):
        for discriminator, field in self.type_map.values():
            if self.type_ == discriminator:
                return getattr(self, field)
        return None

    def _set_value(self, value):
        py_type = type(value)
        if py_type not in self.type_map:
            raise TypeError(py_type)

        for field_type in self.type_map:
            discriminator, field = self.type_map[field_type]
            field_value = None
            if py_type == field_type:
                self.type_ = discriminator
                field_value = value
            if field is not None:
                setattr(self, field, field_value)

    def _del_value(self):
        self._set_value(None)

    value = property(_get_value, _set_value, _del_value, doc=
                     """The logical value of this property.""")

    def __repr__(self):
        return '<%s %r=%r>' % (self.__class__.__name__, self.key, self.value)
