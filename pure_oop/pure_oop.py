#!/usr/bin/env python3

def create_class(*, __super__=None, **kwargs):
    ''' Creates a 'class', possibly based on already created class
        All class attributes are expected in the kwargs, e.g. **locals()
        Atributes are stored in a dictionary.
        Entry point to a class is the 'get' function (closure)
    '''
    def new(self=None, **kwargs):
        ''' Creates a new object.
            All object attributes are expected in hte kwargs

            self is not used and defined as a bypass a general situation,
            when functions are call with an object or class as a 1st argument

            Every object has a reference to its class in the '__class__' key

            Objects are stored in dictionaries and addressed only via the 'get'
            function (closure) to prevent a direct modification of attributes
        '''
        __object__ = dict(**kwargs)
        __object__['__class__'] = __class__

        # If an '__init__' function is defined in the class, run it on the object
        if '__init__' in __class__:
            __class__['__init__'](__object__)

        # This 'get' function belongs to an Object. 
        # It's used as en entry point to object's attributes
        def get(attr=None):
            if attr is None:
                # Without arguments it prints the whole object (dictionary)
                return __object__ 
            elif attr in __object__:
                return __object__[attr]
            elif attr in __class__:
                # Didn't find in an object, but found in a class
                # If it's a function, let's create a method by adding the object
                if callable(__class__[attr]):
                    def method(*args, **kwargs):
                        return __class__[attr](__object__, *args, **kwargs)
                    return method
                else:
                    # If it's a variable, simply return it
                    return __class__[attr]
            elif __class__['__super__'] is not None:
                # If a class of the object has a super class (it was inherited 
                # from another class), then ask its parent class to find
                # the attribute up to the base class through the whole hierarchy
                # and provide it with the object
                return __class__['__super__'](attr, __object__=__object__)
            else:
                # There is no super class, which means it's a base class and
                # there is no the attribute anywhere else
                raise KeyError(f'ERROR: there is no key {attr} in the base class/object')
        return get

    # This 'get' function belongs to a Class. 
    # It's used as en entry point to class' attributes
    # 'object' appears as an argument if request originaly came from an object
    def get(attr=None, *, __object__=None):
        if attr is None:
            return __class__
        elif attr in __class__:
            if callable(__class__[attr]):
                if __object__ is not None:
                    # If an object was provided, then request has come from
                    # that object and it will be set as a first argument.
                    # Make a method by binding a function of a super class
                    # and an object (running inherited functions on an object)
                    def object_method(*args, **kwargs):
                        return __class__[attr](__object__, *args, **kwargs)
                    return object_method
                else:
                    # When object wasn't provided, that means a class was
                    # queried directly and it will be set as a first argument
                    # This allows to have a pure class methods which work 
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
            raise KeyError(f'ERROR: there is no key "{attr}" in any upper classes')

    # Add function's formal parameters and all local names as attributes
    __class__ = locals()
    del(__class__['kwargs'])
    __class__ = { **__class__, **kwargs }

    return get
