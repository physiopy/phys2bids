#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for acqknowledge files.
"""
from bioread import read_file

from phys2bids.physio_obj import blueprint_input, blueprint_output


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input
    """        

    data = read_file(filename).channels
    
    freq = [data[chtrig].samples_per_second] * 2
    timeseries = [data[chtrig].time_index, data[chtrig].data]
    units = ['s', data[chtrig].units]
    names = ['time','trigger']

    k = 0
    for ch in data:
        if k != chtrig:
            print(f'{k:02d}. {ch}')
            timeseries.append(ch.data)
            freq.append(ch.samples_per_second)
            units.append(ch.units)
        k += 1

    return phys_input = blueprint_input(timeseries, freq, names, units)
