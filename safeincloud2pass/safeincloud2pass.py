# -*- coding: utf-8 -*-
"""Manage a LMS-style tipping competion on Reddit.com.

Usage:

"""
# IMPORTS
import argparse
import subprocess
import xml.etree.ElementTree


class Card(object):
    """Represents a SafeInCloud "card"."""

    def __init__(self, node, fields):
        """Init card from supplied xml nodes.

        node - <card> tag as xml.etree.ElementTree node
        fields - list of Field objects from this card's <field> children
        """
        self.load_from_xml_node(node)
        self.fields = fields

    def load_from_xml_node(self, node):
        """Populate from xml.etree <card> data."""
        self.title = node.attrib.get('title')
        self.symbol = node.attrib.get('symbol')
        self._template = node.attrib.get('template', False)
        self._deleted = node.attrib.get('deleted', False)
        self.notes = node.attrib.get('notes')

        try:
            self.label_id = node.find('label_id').text
        except AttributeError:
            self.label_id = None

    @property
    def template(self):
        """Evalute if this card is a template."""
        return str2bool(self._template)

    @property
    def deleted(self):
        """Evalute if this card is a deleted card."""
        return str2bool(self._deleted)

    @property
    def sample(self):
        """Guess if a card is one of the default sample cards.

        There is no attribute to denote a card as a sample, however
        SafeInCloud default sample cards have (Sample) in their title.
        """
        if '(Sample)' in self.title:
            return

    def __str__(self):
        """Output suitable for pass insert --multiline.

        SafeInCloud supports multiple passwords per card. We assume that the
        first password in a card is the primary. Additional passwords are
        appended below with the other attributes.
        """
        result = ''
        primary_password = None
        for field in self.fields:
            if field.type_ == 'password':
                result += field.value + '\n'
                primary_password = field.value
                break
        for field in self.fields:
            if field.type_ == 'password' and field.value == primary_password:
                continue
            else:
                result += str(field) + '\n'
        return result

    def make_path(self, labels):
        """.

        labels - a list of Label objects
        """
        for label in labels:
            if label.id == self.label_id:
                return label.name + '/' + self.name


class Field(object):
    """Fields are the actual name-value pairs stored in a card."""

    def __init__(self, node):
        """Init Field from supplied xml node.

        node - <field> tag as xml.etree.ElementTree node
        """
        self.load_from_xml_node(node)

    def load_from_xml_node(self, node):
        """Populate from xml.etree <field> data."""
        self.name = node.attrib.get('name')
        self.type_ = node.attrib.get('type')
        self.value = node.text

    def __str__(self):
        """Basic output suitable for use as part of pass insert --multiline."""
        return '{}: {}'.format(self.name, self.value)


class Label(object):
    """Simple holder object for a SafeInCloud label."""

    def __init__(self, node):
        """Populate from xml.etree <label> data."""
        self.load_from_xml_node(node)

    def load_from_xml_node(self, node):
        """Populate from xml.etree <label> data."""
        self.name = node.attrib['name']
        self.id = node.attrib['id']


# FUNCTIONS
def str2bool(s):
    """Convert string 'true'/'false' bools to actual bools.

    Boolean XML attributes come back as 'true' or 'false' strings. In Python,
    any non-empty string evaluates to True, so we have to sort these out
    ourselves.
    """
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
    """Return a list of Card objects from all <card> elements under xmlroot."""
    card_nodes = [card for card in xmlroot.iter('card')]
    all_cards = []
    for node in card_nodes:
        fields = [Field(f_node) for f_node in node.iter('field')]
        card = Card(node, fields)
        all_cards.append(card)

    return all_cards


def get_labels(xmlroot):
    """Return a list of Label objects from <label> elements under xmlroot."""
    return [Label(node) for node in xmlroot.iter('label')]


def main(args):
    """Main function for safeincloud2pass."""
    # arguments
    argparse_desc = '''Import SafeInCloud data to pass'''
    parser = argparse.ArgumentParser(description=argparse_desc)
    parser.add_argument('xmlfile', type=str,
                        help='Path to SafeInCloud .xml export file.')
    parser.add_argument('--dryrun', action='store_true',
                        help='Skip samples')
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
    all_labels = get_labels(xmlroot)

    for card in all_cards:

        if not args.showsamples and card.sample:
            continue

        if not args.showtemplates and card.template:
            continue

        if not args.showdeleted and card.deleted:
            continue

        print(card)

        path = card.title
        for label in all_labels:
            # print(label.id)
            # print(card.label_id)
            if label.id == card.label_id:
                path = label.name + '/' + path
        print(path)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
