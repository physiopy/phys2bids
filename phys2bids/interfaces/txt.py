#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phys2bids interface for txt files.
"""

import numpy as np
from phys2bids.physio_obj import BlueprintInput


def labchart_read(channel_list, chtrig, header=[]):
    """
    Reading function for Labchart files
    
    Parameters
    ----------
    channel_list: list
        list with channels only
    chtrig : int
        index of trigger channel
    header: list
        list with that contains file header
    
    Returns
    -------
    BlueprintInput
    
    Raises
    ------
    ValueError
        If len(header) == 0 and therefore there is no header
        If sampling is not in ['hr', 'min', 's', 'ms', 'µs'] reference:
        https://www.adinstruments.com/support/knowledge-base/how-can-channel-titles-ranges-intervals-etc-text-file-be-imported-labchart
    
    See Also
    --------
    physio_obj.BlueprintInput
    """
    # get frequency
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    interval = header[0][1].split(" ")
    if interval[-1] not in ['hr', 'min', 's', 'ms', 'µs']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a valid LabChart'
                             'time unit, this probably means your file is not in Labchart format')

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
    orig_units = []
    for item in range_list:
        orig_units.append(item.split(' ')[1])
    units = ['s', 'V']
    orig_units.pop(chtrig - 1)
    units = units + orig_units
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


def acq_read(channel_list, chtrig, header=[]):
    """
    Reading function for acq files in txt format
    
    Parameters
    ----------
    channel_list: list
        list with channels only
    chtrig : int
        index of trigger channel
    header: list
        list with that contains file header
    
    Returns
    -------
    BlueprintInput
    
    Raises
    ------
    ValueError
        If len(header) == 0 and therefore there is no header

    Warning    
    If sampling is not in ['hr', 'min', 'sec', 'µsec', 'msec']
    
    See Also
    --------
    physio_obj.BlueprintInput
    """
    # get frequency
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    interval = header[1][0].split()
    if interval[-1].split('/')[0] not in ['hr', 'min', 'sec', 'µsec', 'msec']:
        raise Warning(f'Interval unit "{interval[-1]}" is not in a valid AcqKnowledge format'
                        'time unit, this probably means your file is not in'
                        'hr, min, sec, msec or µsec, treating the file as it was sec')
    interval[-1] = interval[-1].split('/')[0]
    if interval[-1] != 'sec':
        print('Interval is not in seconds. Converting its value.')
        if interval[-1] == 'hr':
            interval[0] = float(interval)[0] * 3600
            interval[-1] = 's'
        elif interval[-1] == 'min':
            interval[0] = float(interval[0]) * 60
            interval[-1] = 's'
        elif interval[-1] == 'msec':
            interval[0] = float(interval[0]) / 1000
            interval[-1] = 's'
        elif interval[-1] == 'µsec':
            interval[0] = float(interval[0]) / 1000000
            interval[-1] = 's'
    else:
        interval[0] = float(interval[0])
        interval[-1] = 's'
    # get units and names
    orig_units = []
    orig_names = []
    # the for loop starts at index1 at 3 because that's the first line of the header
    # with channel name info and ends in 2 + twice the number of channels because
    # that should be the last channel name
    for index1 in range(3, 3 + len(header[-1]) * 2, 2):
        orig_names.append(header[index1][0])
        # since units are in the line imediately after we get the units at the same time
        orig_units.append(header[index1 + 1][0])
    # reorder channels names
    names = ['time', 'trigger']
    orig_names.pop(chtrig - 1)
    names = names + orig_names
    # reoder channels units
    units = ['s', 'Volts']
    orig_units.pop(chtrig - 1)
    units = units + orig_units
    # get channels
    timeseries = np.matrix(channel_list).T.tolist()
    freq = [1 / interval[0]] * len(timeseries)
    timeseries = [np.array(darray) for darray in timeseries]
    duration = (timeseries[0].shape[0] + 1) * interval[0]
    t_ch = np.ogrid[0:duration:interval[0]][:-1]  # create time channel
    ordered_timeseries = [t_ch, timeseries[chtrig - 1]]
    timeseries.pop(chtrig - 1)
    ordered_timeseries = ordered_timeseries + timeseries
    return BlueprintInput(ordered_timeseries, freq, names, units)


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input, extracts header and deduces from it
    the format file, afterwards it passes the needed information to
    the corresponding reading function.
    
    Parameters
    ----------
    filename: str
        path to the txt Labchart file
    chtrig : int
        index of trigger channel
    
    Returns
    -------
    phys_in
        Raises
    ------
    
    ValueError
        If len(header) == 0 and therefore there is no header
        If files are not in acq or txt format
    
    Notes
    ------
    multifrequency not detected yet
    
    See Also
    --------
    physio_obj.BlueprintInput
    """

    header = []
    channel_list = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            if line[-1] == '':
                line.remove('')  # sometimes there is an extra space
            for item in line:
                if '#' == item[0]:  # detecting comments
                    line.remove(item)
            if line[-1] == '':
                line.remove('')
            try:
                float(line[0])
            except ValueError:
                header.append(line)
                continue
            line = [float(i) for i in line]
            channel_list.append(line)
        if len(header) == 0:
            raise AttributeError('Files without header are not supported yet')
        elif 'Interval=' in header[0]:
            print('phys2bids detected that your file is in Labchart format')
            phys_in = labchart_read(channel_list, chtrig, header)
        elif 'acq' in header[0][0]:
            print('phys2bids detected that your file is in AcqKnowledge format')
            phys_in = acq_read(channel_list, chtrig, header)
        else:
            raise AttributeError('This file format is not supported yet for txt files')
    return phys_in
