#!/usr/bin/env python

# Name: setup.py
# Purpose: xrcform distutils install program
# Author: Tobias Eberle <tobias.eberle@tobiaseberle.de>
#
# Copyright 2010


NAME    = 'xrcform'
VERSION = '0.1'

AUTHOR       = 'Tobias Eberle'
AUTHOR_EMAIL = 'tobias.eberle@tobiaseberle.de'

LICENSE    = 'GPLv3'
DESCRPTION = 'A library for helping loading GUI from XRC file easily'

PACKAGE_DIR = {'': 'lib'}
PY_MODULES  = ['xrcform']

execfile('metasetup.py')
