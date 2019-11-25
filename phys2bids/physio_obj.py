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
    !!! Pay attention: there's rules on how to populate this object.
    See below ("Attention") !!!

    Input (Properties)
    ------------------
    timeseries : (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first, trigger the second.
        Contains all the timeseries recorded.
        Supports different frequencies!
    freq : (ch) list of floats
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
        Support different frequencies!
    ch_name : (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    units : (ch) list of strings
        List of the units of the channels.

    Properties
    ---------------------
    ch_amount: int
        Number of channels (ch).

    Methods
    -------
    check_trigger_amount :
        Method that counts the amounts of triggers and corrects time offset
        in "time" ndarray.

    Attention
    ---------
    The timeseries (and as a consequence, all the other properties)
    should start with an entry for time and an entry for trigger.
    Both should have the same length - hence same sampling. Meaning:
    - timeseries[0] → ndarray representing time
    - timeseries[1] → ndarray representing trigger
    - timeseries[0].shape == timeseries[1].shape

    As a consequence:
    - freq[0] == freq[1]
    - ch_name[0] = 'time'
    - ch_name[1] = 'trigger'
    - units[0] = 's'
    - Actual number of channels (ANC) +1 <= ch_amount <= ANC +2
    """
    def __init__(self, timeseries, freq, ch_name, units):
        self.timeseries = is_valid(timeseries, list, list_type=np.ndarray)
        self.ch_amount = len(self.timeseries)
        self.freq = has_size(is_valid(freq, list,
                                      list_type=(int, float)),
                             self.ch_amount, 0)
        self.ch_name = has_size(ch_name, self.ch_amount, 'unknown')
        self.units = has_size(units, self.ch_amount, '[]')

    def return_index(cls, idx):
        """
        Method that returns all the proper list entry of the
        properties of the object, given an index.
        """
        return (cls.timeseries[idx], cls.ch_amount, cls.freq[idx],
                cls.ch_name[idx], cls.units[idx])

    def delete_at_index(cls, idx):
        """
        Method that returns all the proper list entry of the
        properties of the object, given an index.
        """
        del(cls.timeseries[idx])
        del(cls.freq[idx])
        del(cls.ch_name[idx])
        del(cls.units[idx])

    def check_trigger_amount(cls, thr=2.5, num_tps_expected=0, tr=0):
        """
        Method that counts trigger points and corrects time offset in
        the list representing time.

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
        trigger_deriv = np.diff(cls.timeseries[1])
        tps = trigger_deriv > thr
        num_tps_found = tps.sum()
        time_offset = cls.timeseries[0][tps.argmax()]

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

        cls.timeseries[0] -= time_offset


class blueprint_output():
    """
    Main output object for phys2bids.
    Contains the blueprint to be exported.

    Properties - Input
    ------------------
    timeseries : (ch x tps) :obj:`numpy.ndarray`
        Numpy 2d array of timeseries
        Contains all the timeseries recorded.
        Impose same frequency!
    freq : float
        Shared frequency of the object.
            Properties
    ch_name : (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    units : (ch) list of strings
        List of the units of the channels.
    start_time : float
        Starting time of acquisition (equivalent to first TR,
        or to the opposite sign of the time offset).

    Methods
    -------
    init_from_blueprint:
        method to populate from input blueprint instead of init
    """
    def __init__(self, timeseries, freq, ch_name, units, start_time):
        self.timeseries = is_valid(timeseries, np.ndarray)
        self.ch_amount = self.timeseries.shape[0]
        self.freq = is_valid(freq, (int, float))
        self.ch_name = has_size(ch_name, self.ch_amount, 'unkown')
        self.units = has_size(units, self.ch_amount, '[]')
        self.start_time = start_time

    def return_index(cls, idx):
        """
        Method that returns all the proper list entry of the
        properties of the object, given an index.
        """
        return (cls.timeseries[idx], cls.ch_amount, cls.freq,
                cls.ch_name[idx], cls.units[idx], cls.start_time)

    def delete_at_index(cls, idx):
        """
        Method that returns all the proper list entry of the
        properties of the object, given an index.
        """
        del(cls.timeseries[idx])
        del(cls.ch_name[idx])
        del(cls.units[idx])

    @classmethod
    def init_from_blueprint(cls, blueprint):
        """
        Method to populate the output blueprint using blueprint_input.

        Input
        -----
        blueprint: :obj: blueprint_input
            the input blueprint object
        """
        timeseries = np.asarray(blueprint.timeseries)
        freq = blueprint.freq[0]
        ch_name = blueprint.ch_name
        units = blueprint.units
        start_time = timeseries[0, 0]
        return cls(timeseries, freq, ch_name, units, start_time)
