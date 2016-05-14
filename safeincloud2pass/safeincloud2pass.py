# -*- coding: utf-8 -*-
"""Manage a LMS-style tipping competion on Reddit.com.

Usage:

"""
# IMPORTS
import argparse
import texttable
import xml.etree.ElementTree


# OBJECTS
class Card(object):
    """Represents a SafeInCloud record."""

    pass


def main(args):
    """Main function for safeincloud2pass."""
    # arguments
    argparse_desc = '''Import SafeInCloud data to pass'''
    parser = argparse.ArgumentParser(description=argparse_desc)
    parser.add_argument('xmlfile', type=str,
                        help='Path to SafeInCloud .xml export file.')
    # TODO: include deleted bool
    # TODO: ignore samples bool
    args = parser.parse_args()

    tree = xml.etree.ElementTree.parse(args.xmlfile)
    root = tree.getroot()

    for card in root.iter('card'):
        # get data
        title = card.attrib['title']

        # init table
        table = texttable.Texttable()
        table.set_cols_align(['c', 'c', 'c'])
        table.set_cols_valign(['m', 'm', 'm'])
        table.header(['Name', 'Type', 'Value'])

        # add data to table
        for field in card.iter('field'):
            table.add_row([field.attrib['name'], field.attrib['type'],
                          field.text])

        # display
        print(title)
        print(table.draw() + "\n")

        # input
        choice = input('Choose to (i)nsert card, (s)kip card or (q)uit: ')

        if choice.lower() == 'i':
            # insert
            pass
        elif choice.lower() == 's':
            # skip card
            pass
        elif choice.lower() == 'q':
            return


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
