# safeincloud2pass.py: Import a SafeInCloud XML export file to pass.

## Introduction
This is a simple script that allows you to import your SafeInCloud Password
Manager data into Pass, *"the standard unix password manager."*

Export your SafeInCloud password database, using the XML option. This must be
done via the (free) Windows application. Unfortunately, at this point the
SafeinCloud Android app does not have an export option.

The exported XML data will include any template cards (SafeInCloud refers to
username/password entries as "cards"), any sample cards, and also any deleted
cards - apparently when you delete a card in SafeIncloud, it is not actually
deleted, but just hidden, and these cards turn up in the export data.
Templates, samples, and deleted cards are filtered out by default, and will
not be imported into pass, unless specifed by the arguments shown below.

## Requirements
Python:     safeincloud2pass should run on any recent version of Python 3. It
does not require any extra libraries.
Pass:       a setup and working installation of pass

## Installation:
git clone this repository or just download
safeincloud2pass/safeincloud2pass.py.

## Usage:
safeincloud2pass.py xmlfile [--samples] [--templates] [--deleted]

## Arguments:
xmlfile         path to SafeInCloud xml export file (required)
--samples       include sample cards (optional)
--templates     include template cards (optional)
--deleted       include deleted cards (optional)
