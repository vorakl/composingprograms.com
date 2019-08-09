#!/usr/bin/env python3

# An example of using the Constraint Programming (CP) paradigm and the Message passing
#
# This module provides two basic abstractions (connectors and constraints) 
# which allow to build a network representing a certain constraint system
#
# Connectors represent a value that can be set/get either directly or by 
# the linked constraint (node) during a propagation of a new value.
# Changing a value of any connector leads to sending the "update" message to 
# a linked node (constraint) and recalculating new values for its other linked
# connectors accordingly to its constraints.
#
# Constraints play a role of a node that keeps constraints and when receives
# the "update" message from any of its connectors, recalculates proper values
# for other connectors and send to them the "set" message with a new value, so
# they can update their state and notify other linked constraints that
# the value changed.
#
# connector-- constraint (node) --connector-- constraint (node) --connector

# A custom exception for values which don't meet their Domains on connectors
class ValueOutOfDomain(Exception):
    def __init__(self, conn, value):
        self.conn_name = conn['name']
        self.value = value

    def __str__(self):
        return f'There is an attempt to assign a wrong value \'{self.value}\' to a connector \'{self.conn_name}\''

def connector(name=None, domain=None):
    ''' An abstract connector between constraints. 
        It represents a value which can be set or automaticaly calculated
        A value might have a Domain
    '''       

    constraints = list()

    def connect(constraint):
        constraints.append(constraint)

    def get_constraints():
        return constraints

    def set_value(src_constr, value):
        if (not domain is None) and (not domain(value)):
            raise ValueOutOfDomain(link, value)
        link['value'] = value
        for constraint in constraints:
            if constraint is not src_constr:
                constraint['update'](link)

    # A dispatch dictionary
    link = { 'name': name,
             'value': None,
             'connect': connect,
             'set': set_value,
             'constraints': get_constraints }

    return link

def constraint(conn1, conn2, constr1, constr2):
    ''' An abstract constraint for two connectors.
        It calculates a new value for one connector when gets the "update" 
        message from another connector (which means a system is changing)
    '''

    def update(src_conn):
        if src_conn is conn1:
            conn2['set'](node, constr1(conn1['value']))
        else:
            conn1['set'](node, constr2(conn2['value']))

    # A dispatch dictionary
    node = { 'name': f'Constraint for \'{conn1["name"]}\' and \'{conn2["name"]}\'',
             'update': update }

    for conn in (conn1, conn2):
        conn['connect'](node)

    return node

