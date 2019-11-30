#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for txt files.
"""

from phys2bids.physio_obj import BlueprintInput

import numpy as np
def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input
    for now this works only with labchart files
    """
    header = []
    channel_list = []
    with open(filename,'r') as f:
        header_l = 0
        for line in f:
            line=line.rstrip('\n').split('\t')
            try: 
                float(line[0])
            except ValueError:
                header.append(line)
                continue 
            line = [float(i) for i in line]
            channel_list.append(line)
    # get frequency 
    interval = header[0][1].split(" ")
    if interval[-1] not in ['hr', 'min', 's','ms','µs']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a valid LabChart time unit, '
                             'this probably means your file is not in labchart format')

    if interval[-1] != 's':
        print(f'interval is not in s converting')
        if interval[-1] == 'hr':
            interval[0] = float(interval)[0]*3600
            interval[-1] = 's'
        elif interval[-1] == 'min':
            interval[0] = float(interval[0])*60
            interval[-1] = 's'
        elif interval[-1] == 'ms':
            interval[0] = float(interval[0])/1000
            interval[-1] = 's'
        elif interval[-1] == 'µs':
            interval[0] = float(interval[0])/1000000
            interval[-1] = 's'
    else:
        interval[0] = float(interval[0])
    # get units
    range_list = header[5][1:]
    units = []
    for item in range_list:
        units.append(item.split(' ')[1])
    # get names
    header[4][1:]
    names = ['time']+header[4][1:]
    # get channels 
    timeseries = np.matrix(channel_list).T.tolist()
    freq = [1/interval[0]]*len(timeseries)
    timeseries=[np.array(darray) for darray in timeseries]
    return BlueprintInput(timeseries, freq, names, units)
