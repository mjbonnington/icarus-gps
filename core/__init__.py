#!/usr/bin/python

# [Icarus] __init__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# Initialise main pipeline environment on package import.


from . import icarus__env__
icarus__env__.set_env()
