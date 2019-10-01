#!/usr/bin/env python3

import pure_oop as oop
from pprint import pprint as pp


def make_c1():
    level = 'c1'
    total = 0

    def __init__(self):
        if ('init' not in self) or (not self['init']):
            self['init'] = level

    # class method. 'self' contains a class
    def instances(self, amount=None):
        # check if self is a class, not an object
        if '__class__' in self:
            raise KeyError(
                        'ERROR: a class function can\'t be run on an object!')
        if amount is not None:
            self['total'] += amount
        return self['total']

    return oop.create_class(**locals())


def make_c2(*, __super__):
    level = 'c2'
    return oop.create_class(**locals())


def make_c3(*, __super__):
    level = 'c3'

    def __init__(self):
        # Calls a class method to update class attributes.
        # This class method exists in c1 but it doesn't matter via which
        # classes to invoke it. The easiest way is starting right from its
        # own class and a method will be found up through the hierarchy.
        self['__class__']['get']('instances')(1)

        # ask a super class to find '__init__' up to the base class
        # and initialize this object
        self['__class__']['__super__']('__init__', __object__=self)()

    return oop.create_class(**locals())

c1 = make_c1()
c2 = make_c2(__super__=c1)
c3 = make_c3(__super__=c2)

o2 = c2('new')()
# there is no __init__ in c2, so, add +1 to instances here
c2('instances')(1)

o3 = c3('new')(age=37, name='Alan')

print('\no2 object attributes:')
pp(o2())
print('\no3 object attributes:')
pp(o3())

print("\nc1's class attribute 'total' requested by o3: {}".format(
                                                                  o3('total')))
print("The same attribute requested via c2's class method: {}".format(
                                                            c2('instances')()))
