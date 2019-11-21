#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for acqknowledge files.
"""
from bioread import read_file

from phys2bids.physio_obj import blueprint_input, blueprint_output


def print_info_acq(filename, data):
    """
    Print the info of acq files
    """
    print(f'File {filename} contains:\n')
    for ch in range(0, len(data)):
        print(str(ch) + ': ' + data[ch].name)


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input
    """        

    data = read_file(filename).channels
    phys_input = blueprint_input()


