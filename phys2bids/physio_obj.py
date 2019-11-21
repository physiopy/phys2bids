#!/usr/bin/env python3

"""
I/O objects for phys2bids.
"""

from numpy import ndarray, shape


def is_valid(var, type, list_type=None, return_var=True):
    """
    Checks that the var is of a certain type.
    If type is list and list_type is specified,
    checks that the list contains list_type.
    Input
    -----
    var:
        Variable to be checked.
    type: type
        Type the variable is assumed to be.
    list_type: type
        As type.

    Output
    ------
    var:
        Variable to be checked (same as input).
    """
    if not isinstance(var, type):
        raise AttributeError('Something went wrong while populating physio_io!')

    if type is list and list_type is not None:
        for element in var:
            is_valid(element, list_type, return_var=False)

    if return_var:
        return var


def has_data_size(var, data, token):
    """
    Checks that the var has the same dimension of the data
    If it's not the case, fill in the var or removes exceding var entry.
    Input
    -----
    var:
        Variable to be checked.
    data: (ch, [tps]) list or :obj:`numpy.ndarray`
        Actual timeseries data.
    token:
        What to be used in case of completion.

    Output
    ------
    var:
        Variable to be checked (same as input).
    """
    if isinstance(data, list):
        data_size = len(data)
    elif isinstance(data, ndarray):
        data_size = data.shape[0]
    else:
        raise Exception('Something went wrong assessing data size')

    if len(var) > data_size:
        var = var[:data_size]

    if len(var) < data_size:
        var = var + [token] * (data_size - len(var))

    return var


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
        self.ch_name = is_valid(ch_name, list, list_type=str)
        self.units = is_valid(units, list, list_type=str)


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
        self.timeseries = is_valid(diff_timeseries, list, list_type=ndarray)
        self.freq = has_data_size(is_valid(diff_freq, list,
                                           list_type=(int, float)),
                                  self.timeseries, 0)
        self.ch_name = has_data_size(self.ch_name, self.timeseries, 'missing')
        self.units = has_data_size(self.units, self.timeseries, '[]')


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
        self.timeseries = is_valid(timeseries, ndarray)
        self.freq = has_data_size(is_valid(freq, (int, float)), [1], 0)
        self.ch_name = has_data_size(self.ch_name, self.timeseries, 'missing')
        self.units = has_data_size(self.units, self.timeseries, '[]')
