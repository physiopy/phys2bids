#!/usr/bin/env python3

"""
I/O objects for phys2bids
"""

import numpy as np

def is_valid(var, type, list_type):
    """
    Checks that the var is of a certain type.
    If type is list and list_type is specified,
    checks that the list contains
    """



class phys_io():
    """
    Parent class for i/o physio objects.

    Properties
    ----------
    ch_name: (ch, ) list
        List of channel names - one per channel
    units: (ch, ) list
        list of channel frequencies - one per channel
    """
    def __init__(self, ch_name, units):
        self.ch_name = ch_name
        self.units = units


class phys_input(phys_io):
    """
    Main input object for phys2bids.
    Contains the schema to be populated.

    Properties
    ----------
    timeseries : (ch, [tps]) list
        List of numpy 1d arrays - one for channel.
        Contains all the timeseries recorded.
        Supports different frequencies!
    freq : (ch, ) list
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
        Support different frequencies!
    """
    def __init__(self, diff_timeseries, diff_freq, ch_name, units):
        super().__init__(ch_name, units)
        self.timeseries = diff_timeseries
        self.freq = diff_freq


class phys_output(phys_io):
    """
    Main output object for phys2bids.
    Contains the schema to be exported.

    Properties
    ----------
    timeseries : (ch x tps) :obj:`numpy.ndarray`
        Numpy 2d array of timeseries
        Contains all the timeseries recorded.
        Impose same frequency!
    freq : float
        Shared frequency of the object.
    """
    def __init__(self, timeseries, freq, ch_name, units):
        super().__init__(ch_name, ch_name, units)
        self.timeseries = timeseries
        self.freq = freq
        