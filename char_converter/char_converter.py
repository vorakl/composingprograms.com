#!/usr/bin/env python3

# The example of implementing a constraint programming for converting Characters to/from Ascii codes
#
# The System (a network built of connectors and constraints):
# small ascii <-> (code) <-> small letter <-> (aA) <-> capital letter <-> (code) <-> capital ascii
#
# A system allows to set a value of any connector and get a calculated result
# on all other connectors by propagating updates using the Massage passing approach

import constraint_programming as cp

def code(conn1, conn2):
    ''' A particular constraint for converting Chars to/from Ascii codes '''
    return cp.constraint(conn1, conn2, ord, chr)

def aA(conn1, conn2):
    ''' A particular constraint for converting small to/from Capital letters '''
    return cp.constraint(conn1, conn2, str.upper, str.lower)

def show_connectors(connectors):
    sa, sl, ca, cl = connectors
    print(f"Small letter \'{sl['value']}\' with ascii code {sa['value']}")
    print(f"Capital letter \'{cl['value']}\' with ascii code {ca['value']}\n")

def main():
    # An example of recalculation of all values by changing different parts
    # of the system and propagating these values across the system

    # Set up a Network
    # Create all connectors (with their Domains) accordingly to our Network
    small_ascii = cp.connector('Small Ascii', lambda x: x >= 97 and x <= 122)
    small_letter = cp.connector('Small Letter', lambda x: x >= 'a' and x <= 'z')
    capital_ascii = cp.connector('Capital Ascii', lambda x: x >= 65 and x <= 90)
    capital_letter = cp.connector('Capital Letter', lambda x: x >= 'A' and x <= 'Z')
    connectors = (small_ascii, small_letter, capital_ascii, capital_letter)

    # Link connectors with Nodes (constraints)
    code(small_letter, small_ascii)
    code(capital_letter, capital_ascii)
    aA(small_letter, capital_letter)

    # Change values of different connectors and see what happens
    small_letter['set'](None, 'c')
    show_connectors(connectors)

    capital_ascii['set'](None, 65)
    show_connectors(connectors)

    capital_letter['set'](None, 'X')
    show_connectors(connectors)

    # This fails because a value is out of the Domain. 
    # The system's state doesn't change
    try:
        capital_ascii['set'](None, 100)
    except cp.ValueOutOfDomain as err:
        print(f'ERROR: {err}')
    show_connectors(connectors)

if __name__ == '__main__':
    main()

