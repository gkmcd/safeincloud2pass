# -*- coding: utf-8 -*-
"""Manage a LMS-style tipping competion on Reddit.com.

Usage:

"""
# IMPORTS
import argparse
import texttable
import subprocess
import xml.etree.ElementTree


class Card(object):
    """Represents a SafeInCloud "card"."""

    def __init__(self, xml_data, fields):
        """."""
        self.load_from_from_xml(xml_data)
        self.fields = fields

    def load_from_from_xml(self, xml_data):
        """Populate from xml.etree data."""
        self.title = xml_data.attrib.get('title')
        self.symbol = xml_data.attrib.get('symbol')
        self._template = xml_data.attrib.get('template', False)
        self._deleted = xml_data.attrib.get('deleted', False)
        self.label = xml_data.attrib.get('label')
        self.notes = xml_data.attrib.get('notes')

    @property
    def template(self):
        """."""
        return str2bool(self._template)

    @property
    def deleted(self):
        """."""
        return str2bool(self._deleted)

    @property
    def sample(self):
        """SafeInCloud default sample cards have (Sample) in their title."""
        if '(Sample)' in self.title:
            return

    def output_for_pass():
        """."""
        pass


class Field(object):
    """Fields are the actual data stored in a card."""

    def __init__(self, xml_data):
        """."""
        self.load_from_xml_data(xml_data)

    def load_from_xml_data(self, xml_data):
        """Populate from xml.etree data."""
        self.name = xml_data.attrib.get('name')
        self.type_ = xml_data.attrib.get('type')
        self.value = xml_data.text

    def output_for_pass():
        """."""
        pass


class Label(object):
    """."""

    def __init__():
        """."""
        pass


# FUNCTIONS
def str2bool(s):
    """XML string bools need to be converted to actual bools."""
    if s is False:
        return False
    elif s in ['False', 'false']:
        return False
    elif s in ['True', 'true']:
        return True


def pass_import_entry(path, data):
    """Import new password to password-store using pass insert command."""
    proc = subprocess.Popen(['pass', 'insert', '--multiline', path],
                            stdin=PIPE, stdout=PIPE)  # noqa
    proc.communicate(data.encode('utf8'))
    proc.wait()


def get_cards(xmlroot):
    """Return a list of Card objects from card xml elements under xmlroot."""
    card_tags = [card for card in xmlroot.iter('card')]
    all_cards = []
    for tag in card_tags:
        fields = [Field(tag) for field in tag.iter('field')]
        card = Card(tag, fields)
        all_cards.append(card)

    return all_cards


def main(args):
    """Main function for safeincloud2pass."""
    # arguments
    argparse_desc = '''Import SafeInCloud data to pass'''
    parser = argparse.ArgumentParser(description=argparse_desc)
    parser.add_argument('xmlfile', type=str,
                        help='Path to SafeInCloud .xml export file.')
    parser.add_argument('--showsamples', action='store_true',
                        help='Skip samples')
    parser.add_argument('--showtemplates', action='store_true',
                        help='Skip templates')
    parser.add_argument('--showdeleted', action='store_true',
                        help='Show deleted cards')
    args = parser.parse_args()

    # load data
    tree = xml.etree.ElementTree.parse(args.xmlfile)
    xmlroot = tree.getroot()

    all_cards = get_cards(xmlroot)

    for card in all_cards:

        if not args.showsamples and card.sample:
            print(card.title + ' is a sample')
            continue

        if not args.showtemplates and card.template:
            print(card.title + ' is a template')
            continue

        if not args.showdeleted and card.deleted:
            print(card.title + ' is deleted')
            continue

        continue

        # init display table
        table = texttable.Texttable()
        table.set_cols_align(['c', 'c', 'c'])
        table.set_cols_valign(['m', 'm', 'm'])
        table.set_cols_dtype(['t', 't', 't'])
        table.header(['Name', 'Type', 'Value'])

        # add data to table
        for field in card.iter('field'):
            table.add_row([field.attrib['name'], field.attrib['type'],
                          field.text])

        # display
        print('\nCard: {}'.format(title))
        print(table.draw() + "\n")

        # handle input
        while True:
            choice = input('Choose to: (i)nsert card, (s)kip card or (q)uit: ')
            if choice.lower() not in ('i', 's', 'q'):
                print("Not an appropriate choice.\n")
            else:
                break

        # process selection
        if choice.lower() == 'i':
            # construct password store multiline entry

            # SafeInCloud allows multiple password fields
            password_fields = card.findall('field[@type="password"]')

            # take the first password as the primary
            entry = '{}\n'.format(password_fields[0].text)

            # add the others below
            for password in password_fields[1:]:
                entry += '{}: {}\n'.format(password.attrib['name'], field.text)

            # add all other (non-password) fields
            non_password_fields = [x for x in card.iter('field')
                                   if x not in password_fields]
            for field in non_password_fields:
                entry += '{}: {}\n'.format(field.attrib['name'], field.text)

            print(entry)

            # path = keyFolder+"/"+keyName+"/"+username

            # pass_import_entry()

        elif choice.lower() == 's':
            # skip card
            print('Skipping card...')
            print('\n\n')
        elif choice.lower() == 'q':
            return


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
