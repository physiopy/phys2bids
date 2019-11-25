#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
I/O objects for phys2bids.
"""

import numpy as np


def is_valid(var, var_type, list_type=None, return_var=True):
    """
    Checks that the var is of a certain type.
    If type is list and list_type is specified,
    checks that the list contains list_type.
    Input
    -----
    var:
        Variable to be checked.
    var_type: type
        Type the variable is assumed to be.
    list_type: type
        As type.

    Output
    ------
    var:
        Variable to be checked (same as input).
    """
    if not isinstance(var, var_type):
        raise AttributeError('Something went wrong while populating blueprint')

    if var_type is list and list_type is not None:
        for element in var:
            is_valid(element, list_type, return_var=False)

    if return_var:
        return var


def has_size(var, data_size, token):
    """
    Checks that the var has the same dimension of the data
    If it's not the case, fill in the var or removes exceding var entry.
    Input
    -----
    var:
        Variable to be checked.
    data_size: int
        Size of data of interest.
    token:
        What to be used in case of completion.

    Output
    ------
    var:
        Variable to be checked (same as input).
    """
    if len(var) > data_size:
        var = var[:data_size]

    if len(var) < data_size:
        var = var + [token] * (data_size - len(var))

    return var


class blueprint_input():
    """
    Main input object for phys2bids.
    Contains the blueprint to be populated.

    Properties
    ----------
    diff_timeseries : (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first, trigger the second.
        Contains all the timeseries recorded.
        Supports different frequencies!
    diff_freq : (ch) list of floats
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
        Support different frequencies!
    ch_name : (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    units : (ch) list of strings
        List of the units of the channels.

    Methods
    -------
    check_trigger_amount :
        Method that counts the amounts of triggers and corrects time offset.

    """
    def __init__(self, diff_timeseries, diff_freq, ch_name, units):
        self.timeseries = is_valid(diff_timeseries, list, list_type=np.ndarray)
        self.ch_amount = len(self.timeseries)
        self.freq = has_size(is_valid(diff_freq, list,
                                      list_type=(int, float)),
                             self.ch_amount, 0)
        self.ch_name = has_size(ch_name, self.ch_amount, 'unknown')
        self.units = has_size(units, self.ch_amount, '[]')

    def check_trigger_amount(self, thr=2.5, num_tps_expected=0, tr=0):
        """
        Method that counts trigger points and corrects time offset.

        Input
        -----
        thr: float
            threshold to be used to detect trigger points.
            Default is 2.5
        num_tps_expected: int
            number of expected triggers (num of TRs in fMRI)
        tr: float
            the Repetition Time of the fMRI data.
        """
        print('Counting trigger points')
        trigger_deriv = np.diff(self.timeseries[1])
        tps = trigger_deriv > thr
        num_tps_found = tps.sum()
        time_offset = self.timeseries[0][tps.argmax()]

        if num_tps_expected:
            print('Checking number of tps')
            if num_tps_found > num_tps_expected:
                tps_extra = num_tps_found - num_tps_expected
                print(f'Found {tps_extra} tps more than expected!\n'
                      'Assuming extra tps are at the end (try again with a '
                      'more conservative thr)')

            elif num_tps_found < num_tps_expected:
                tps_missing = num_tps_expected - num_tps_found
                print(f'Found {tps_missing} tps less than expected!')
                if tr:
                    print('Correcting time offset, assuming missing tps '
                          'are at the beginning (try again with '
                          'a more liberal thr')
                    time_offset -= (tps_missing * tr)
                else:
                    print('Can\'t correct time offset, (try again specifying '
                          'tr or with a more liberal thr')

            else:
                print('Found just the right amount of tps!')

        else:
            print('Cannot check the number of tps')

        self.timeseries[0] -= time_offset


class blueprint_output():
    """
    Main output object for phys2bids.
    Contains the blueprint to be exported.

    Properties
    ----------
    timeseries : (ch x tps) :obj:`numpy.ndarray`
        Numpy 2d array of timeseries
        Contains all the timeseries recorded.
        Impose same frequency!
    freq : float
        Shared frequency of the object.
    """
    def __init__(self, timeseries, freq, ch_name, units, start_time):
        self.timeseries = is_valid(timeseries, np.ndarray)
        self.ch_amount = self.timeseries.shape[0]
        self.freq = has_size(is_valid(freq, (int, float)), 1, 0)
        self.ch_name = has_size(ch_name, self.ch_amount, 'unkown')
        self.units = has_size(units, self.ch_amount, '[]')
        self.start_time = start_time
