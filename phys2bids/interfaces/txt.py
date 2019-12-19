#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for txt files.
"""

import numpy as np
from phys2bids.physio_obj import BlueprintInput


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input
    for now this works only with labchart files
        Input (Properties)
    ------------------
    filename: str
        path to the txt labchart file
    chtrig : int
        index of trigger channel

    Output
    ------------------
    phys_in: BlueprintInput object for more see BlueprintInput docs
    """

    header = []
    channel_list = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            for item in line:
                if '#' in item:
                    line.remove(item)
            try:
                float(line[0])
            except ValueError:
                header.append(line)
                continue
            line = [float(i) for i in line]
            channel_list.append(line)
        if len(header) == 0:
            raise AttributeError(f'Files without header are not supported yet')
        if 'Interval=' in header[0]:
            print('phys2bids detected that your file is in labchart format')
            phys_in = labchart_read(channel_list, chtrig, header)
    return phys_in


def labchart_read(channel_list, chtrig, header=[]):
    """
    reading function for labchart files
        Input (Properties)
    ------------------
    channel_list: list
        list with channels only
    chtrig : int
        index of trigger channel
    header: list
        list with that contains file header
    Output
    ------------------
    BlueprintInput object for more see BlueprintInput docs
    """
    # get frequency
    if len(header) == 0:
        raise AttributeError(f'Files without header are not supported yet')
    interval = header[0][1].split(" ")
    if interval[-1] not in ['hr', 'min', 's', 'ms', 'µs']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a valid LabChart'
                             'time unit, this probably means your file is not in labchart format')

    if interval[-1] != 's':
        print('Interval is not in seconds. Converting its value.')
        if interval[-1] == 'hr':
            interval[0] = float(interval)[0] * 3600
            interval[-1] = 's'
        elif interval[-1] == 'min':
            interval[0] = float(interval[0]) * 60
            interval[-1] = 's'
        elif interval[-1] == 'ms':
            interval[0] = float(interval[0]) / 1000
            interval[-1] = 's'
        elif interval[-1] == 'µs':
            interval[0] = float(interval[0]) / 1000000
            interval[-1] = 's'
    else:
        interval[0] = float(interval[0])
    # get units
    range_list = header[5][1:]
    units = []
    for item in range_list:
        units.append(item.split(' ')[1])
    # get names
    orig_names = header[4][1:]
    names = ['time', 'trigger']
    orig_names.pop(chtrig - 1)
    names = names + orig_names
    # get channels
    timeseries = np.matrix(channel_list).T.tolist()
    freq = [1 / interval[0]] * len(timeseries)
    timeseries = [np.array(darray) for darray in timeseries]
    ordered_timeseries = [timeseries[0], timeseries[chtrig]]
    timeseries.pop(chtrig)
    timeseries.pop(0)
    ordered_timeseries = ordered_timeseries + timeseries
    return BlueprintInput(ordered_timeseries, freq, names, units)
