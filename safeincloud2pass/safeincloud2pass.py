# -*- coding: utf-8 -*-
"""Manage a LMS-style tipping competion on Reddit.com.

Usage:

"""
# IMPORTS
import argparse
import texttable
import subprocess
import xml.etree.ElementTree


# OBJECTS
class Card(object):
    """Represents a SafeInCloud record."""

    pass


# FUNCTIONS
def pass_import_entry(path, data):
    """Import new password to password-store using pass insert command."""
    proc = subprocess.Popen(['pass', 'insert', '--multiline', path],
                            stdin=PIPE, stdout=PIPE)
    proc.communicate(data.encode('utf8'))
    proc.wait()


def main(args):
    """Main function for safeincloud2pass."""
    # arguments
    argparse_desc = '''Import SafeInCloud data to pass'''
    parser = argparse.ArgumentParser(description=argparse_desc)
    parser.add_argument('xmlfile', type=str,
                        help='Path to SafeInCloud .xml export file.')
    parser.add_argument('--skip_samples', type=bool, default=True,
                        help='Skip samples')
    # TODO: include deleted bool

    args = parser.parse_args()

    tree = xml.etree.ElementTree.parse(args.xmlfile)
    root = tree.getroot()

    for card in root.iter('card'):
        # get data
        title = card.attrib['title']

        if args.skip_samples and '(Sample)' in title:
            continue

        # init display table
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

        # handle input
        while True:
            choice = input('Choose to: (i)nsert card, (s)kip card or (q)uit: ')
            if choice.lower() not in ('i', 's', 'q'):
                print("Not an appropriate choice.")
            else:
                break

        # process selection
        if choice.lower() == 'i':
            # insert
            print('pass insert ')
        elif choice.lower() == 's':
            # skip card
            print('Skipping card...')
            print('\n\n')
        elif choice.lower() == 'q':
            return


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
