#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for acqknowledge files.
"""
from bioread import read_file

from phys2bids.physio_obj import BlueprintInput


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input
    """

    data = read_file(filename).channels

    freq = [data[chtrig].samples_per_second] * 2
    timeseries = [data[chtrig].time_index, data[chtrig].data]
    units = ['s', data[chtrig].units]
    names = ['time', 'trigger']

    for k, ch in enumerate(data):
        if k != chtrig:
            print(f'{k:02d}. {ch}')
            timeseries.append(ch.data)
            freq.append(ch.samples_per_second)
            units.append(ch.units)

    return BlueprintInput(timeseries, freq, names, units)
