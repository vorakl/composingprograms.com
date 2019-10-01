#!/usr/bin/env python3


def create_class(*, __super__=None, **kwargs):
    ''' Creates a class, possibly based on an existing class.
        All initial class attributes are expected to get in the 'kwargs'
        argument, e.g. '**locals()'.

        Atributes are stored in a dictionary.
        Entry point to a class is the 'get' function (closure).
    '''

    def new(self=None, **kwargs):
        ''' Creates a new object.
            All object attributes are expected to get in the 'kwargs' argument.

            self is not used and defined here as a bypass for a general
            situation, when functions are called with an object or a class
            as a 1st argument.

            Every object has a reference to its class in the '__class__'
            attribute. Objects are stored in dictionaries and accessed via
            the 'get' function (closure) to prevent a direct modification
            of attributes.
        '''

        __object__ = dict(**kwargs)
        __object__['__class__'] = __class__

        # If the '__init__' function is defined in a class, then run it
        # for the object
        if '__init__' in __class__:
            __class__['__init__'](__object__)

        def get(attr=None):
            ''' This 'get' function belongs to an object.
                It's used as en entry point to the object's attributes.
            '''

            if attr is None:
                # With no arguments it prints the whole object (dictionary)
                return __object__
            elif attr in __object__:
                return __object__[attr]
            elif attr in __class__:
                # Didn't find in an object, but found in a class.
                # If it's a function, let's create a method by binding
                # to the object
                if callable(__class__[attr]):
                    def object_method(*args, **kwargs):
                        return __class__[attr](__object__, *args, **kwargs)
                    return object_method
                else:
                    # If it's a class attribute (variable), simply return it
                    return __class__[attr]
            elif __class__['__super__'] is not None:
                # If a class of the object has a super class (it was inherited
                # from another class), then ask its parent class to find
                # the attribute up to the base class through the hierarchy.
                return __class__['__super__'](attr, __object__=__object__)
            else:
                # There is no super class, which means it's a base class and
                # there is no the attribute anywhere else
                err = 'ERROR: there is no key {} in the base class/object'
                raise KeyError((err).format(attr))

        return get

    def get(attr=None, *, __object__=None):
        ''' This 'get' function belongs to a class.
            It's used as en entry point to class' attributes.
            '__object__' isn't None if request comes from an object.
        '''

        if attr is None:
            # With no arguments it prints the whole class (dictionary)
            return __class__
        elif attr in __class__:
            if callable(__class__[attr]):
                if __object__ is not None:
                    # If an object was provided, then request has come from
                    # it and this object will be set as a first argument.
                    # Make a method by binding a function of an object's super
                    # class and the object (it will run a function from
                    # an inherited class on an object).
                    def object_method(*args, **kwargs):
                        return __class__[attr](__object__, *args, **kwargs)
                    return object_method
                else:
                    # When object wasn't provided, that means a class was
                    # queried directly and it will be set as a first argument
                    # This allows us to have a pure class methods which work
                    # on thier class attributes only
                    def class_method(*args, **kwargs):
                        return __class__[attr](__class__, *args, **kwargs)
                    return class_method
            else:
                # a simple class attribute (variable)
                return __class__[attr]
        elif __super__ is not None:
            # didn't find an attribute, check on the upper layer
            return __super__(attr, __object__=__object__)
        else:
            # the exception in case of an inheritance
            err = 'ERROR: there is no key "{}" in any upper classes'
            raise KeyError(err).format(attr)

    # Add local names and key-value pairs from 'kwargs' as class' attributes.
    __class__ = {**locals(), **kwargs}
    del(__class__['kwargs'])  # remove unnecessary element from the attributes

    return get
