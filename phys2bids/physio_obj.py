#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""I/O objects for phys2bids."""

import logging
import re
from copy import deepcopy
from itertools import groupby

import numpy as np

TRIGGER_NAMES = ["trig", "trigger"]

LGR = logging.getLogger(__name__)
LGR.setLevel(logging.INFO)


def is_valid(var, var_type, list_type=None):
    """
    Check that the var is of a certain type.

    If type is list and list_type is specified,
    checks that the list contains list_type.

    Parameters
    ----------
    var: any type
        Variable to be checked.
    var_type: type
        Type the variable is assumed to be.
    list_type: type
        Like var_type, but applies to list elements.

    Returns
    -------
    var: any type
        Variable to be checked (same as input).

    Raises
    ------
    AttributeError
        If var is not of var_type
    """
    if not isinstance(var, var_type):
        raise AttributeError(f'The given variable is not a {var_type}')

    if var_type is list and list_type is not None:
        for element in var:
            _ = is_valid(element, list_type)

    return var


def has_size(var, data_size, token):
    """
    Check that the var has the same dimension of the data.

    If it's not the case, fill in the var or removes exceeding var entry.

    Parameters
    ----------
    var: list
        Variable to be checked.
    data_size: int
        Size of data of interest.
    token: same type as `var`
        If `var` doesn't have as many elements as the data_size,
        it will be padded at the end with this `token`.
        It has to be the same type as var.

    Returns
    -------
    var: list
        Variable to be checked (same as input).
    """
    if len(var) > data_size:
        var = var[:data_size]

    if len(var) < data_size:
        _ = is_valid(token, type(var[0]))
        var = var + [token] * (data_size - len(var))

    return var


def are_equal(self, other):
    """
    Return test of equality between two objects.

    The equality is true if two objects are the same or
    if one of the objects is equivalent to the dictionary
    format of the other.
    It's particularly written for Blueprint type objects.
    This function might not work with other classes.

    Parameters
    ----------
    other:
        comparable object.

    Returns
    -------
    boolean
    """

    def _deal_with_dict_value_error(self, other):
        # Check if "self" has a 'timeseries' key. If not, return False.
        try:
            self['timeseries']
        except KeyError:
            return False
        except TypeError:
            return False
        else:
            # Check that the two objects have the same keys.
            # If not, return False, otherwise loop through the timeseries key.
            if self.keys() == other.keys():
                alltrue_timeseries = [False] * len(self['timeseries'])
                alltrue_keys = [False] * len(self)
                for j, key in enumerate(self.keys()):
                    if key == 'timeseries':
                        for i in range(len(self['timeseries'])):
                            alltrue_timeseries[i] = (self['timeseries'][i].all()
                                                     == other['timeseries'][i].all())
                        alltrue_keys[j] = all(alltrue_timeseries)
                    else:
                        alltrue_keys[j] = (self[key] == other[key])
                return all(alltrue_keys)
            else:
                return False

    try:
        # Try to compare the dictionary format of the two objects
        return self.__dict__ == other.__dict__
    except ValueError:
        return _deal_with_dict_value_error(self.__dict__, other.__dict__)
    except AttributeError:
        # If there's an AttributeError, the other object might not be a class.
        # Try to compare the dictionary format of self with the other object.
        try:
            return self.__dict__ == other
        except ValueError:
            return _deal_with_dict_value_error(self.__dict__, other)
        except AttributeError:
            # If there's an AttributeError, self is not a class.
            # Try to compare self with the dictionary format of the other object.
            try:
                return self == other.__dict__
            except ValueError:
                return _deal_with_dict_value_error(self, other.__dict__)
            except AttributeError:
                # If there's an AttributeError, both objects are not a class.
                # Try to compare self with the two object.
                try:
                    return self == other
                except ValueError:
                    return _deal_with_dict_value_error(self, other)


class BlueprintInput():
    """
    Main input object for phys2bids.

    Contains the blueprint to be populated.
    !!! Pay attention: there's rules on how to populate this object.
    See below ("Attention") !!!

    Attributes
    ----------
    timeseries : (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first.
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
    trigger_idx : int
        The trigger index. Optional. Default is 0.
    num_timepoints_found: int or None
        Amount of timepoints found in the automatic count.
        This is initialised as "None" and then computed internally,
        *if* check_trigger_amount() is run.
    thr: float or None
        Threshold used by check_trigger_amount() to detect trigger points.
        This is initialised as "None" and then computed internally,
        *if* check_trigger_amount() is run.
    time_offset: float
        Time offset found by check_trigger_amount().
        This is initialised as 0 and then computed internally,
        *if* check_trigger_amount() is run.

    Methods
    -------
    ch_amount:
        Property. Returns number of channels (ch).
    rename_channels:
        Changes the list "ch_name" in a controlled way.
    return_index:
        Returns the proper list entry of all the
        properties of the object, given an index.
    delete_at_index:
        Returns all the proper list entry of the
        properties of the object, given an index.
    check_trigger_amount:
        Counts the amounts of triggers and corrects time offset
        in "time" ndarray. Also adds property ch_amount.

    Notes
    -----
    The timeseries (and as a consequence, all the other properties)
    should start with an entry for time.
    It should have the same length of the trigger - hence same sampling.
    Meaning:
    - timeseries[0] → ndarray representing time
    - timeseries[chtrig] → ndarray representing trigger
    - timeseries[0].shape == timeseries[chtrig].shape

    As a consequence:
    - freq[0] == freq[chtrig]
    - ch_name[0] = 'time'
    - units[0] = 's'
    - Actual number of channels +1 <= ch_amount
    """

    def __init__(self, timeseries, freq, ch_name, units, trigger_idx,
                 num_timepoints_found=None, thr=None, time_offset=0):
        """Initialise BlueprintInput (see class docstring)."""
        self.timeseries = deepcopy(is_valid(timeseries, list, list_type=np.ndarray))
        self.freq = deepcopy(has_size(is_valid(freq, list,
                                      list_type=(int, float)),
                             self.ch_amount, 0.0))
        self.ch_name = deepcopy(has_size(ch_name, self.ch_amount, 'unknown'))
        self.units = deepcopy(has_size(units, self.ch_amount, '[]'))

        self.trigger_idx = deepcopy(is_valid(trigger_idx, int))
        if trigger_idx == 0:
            self.auto_trigger_selection()
        else:
            if ch_name[trigger_idx] not in TRIGGER_NAMES:
                LGR.info('Trigger channel name is not in our trigger channel name alias list. '
                         'Please make sure you choose the proper channel.')

        self.num_timepoints_found = deepcopy(num_timepoints_found)
        self.thr = deepcopy(thr)
        self.time_offset = deepcopy(time_offset)
        self._time_resampled_to_trigger = None

    @property
    def ch_amount(self):
        """
        Property. Return number of channels (ch).

        Returns
        -------
        int
            Number of channels
        """
        return len(self.timeseries)

    def __getitem__(self, idx):
        """
        Return a copy of the object with a sliced version of self.timeseries.

        The slicing is based on the trigger. If necessary, computes a sort of
        interpolation to get the right index in multifreq.
        If the trigger was not specified, the slicing is based on the time instead.

        Parameters
        ----------
        idx: int, tuple of int or slicer
            indexes to use to slice the timeseries.

        Returns
        -------
        BlueprintInput object
            a copy of the object with the part of timeseries expressed by idx.

        Raises
        ------
        IndexError
            If the idx, represented as a slice, is out of bounds.

        Notes
        -----
        If idx is an integer, it returns an instantaneous moment for all channels.
        If it's a slice, it always returns the full slice. This means that
        potentially, depending on the frequencies, BlueprintInput[1] and
        BlueprintInput[1:2] might return different results.
        """
        sliced_timeseries = [None] * self.ch_amount
        return_instant = False
        if not self.trigger_idx:
            self.trigger_idx = 0

        trigger_length = len(self.timeseries[self.trigger_idx])

        # If idx is an integer, return an "instantaneous slice" and initialise slice
        if isinstance(idx, int):
            return_instant = True

            # If idx is a negative integer, take the idx element from the end.
            if idx < 0:
                idx = trigger_length + idx

            idx = slice(idx, idx + 1)

        # If idx.start or stop are None, make them 0 or trigger length.
        if idx.start is None:
            idx = slice(0, idx.stop)
        if idx.stop is None:
            idx = slice(idx.start, trigger_length)

        # Check that the indexes are not out of bounds
        if idx.start >= trigger_length or idx.stop > trigger_length:
            raise IndexError(f'Slice ({idx.start}, {idx.stop}) is out of '
                             f'bounds for channel {self.trigger_idx} '
                             f'with size {trigger_length}')

        # Operate on each channel on its own
        for n, channel in enumerate(self.timeseries):
            idx_dict = {'start': idx.start, 'stop': idx.stop, 'step': idx.step}
            # Adapt the slicing indexes to the right requency
            for i in ['start', 'stop', 'step']:
                if idx_dict[i]:
                    idx_dict[i] = int(np.floor(self.freq[n]
                                               / self.freq[self.trigger_idx]
                                               * idx_dict[i]))

            # Correct the slicing stop if necessary
            if idx_dict['start'] == idx_dict['stop'] or return_instant:
                idx_dict['stop'] = idx_dict['start'] + 1
            elif trigger_length == idx.stop:
                idx_dict['stop'] = len(channel)

            new_idx = slice(idx_dict['start'], idx_dict['stop'], idx_dict['step'])
            sliced_timeseries[n] = channel[new_idx]

        sliced_bp = BlueprintInput(sliced_timeseries, self.freq, self.ch_name,
                                   self.units, self.trigger_idx,
                                   self.num_timepoints_found, self.thr,
                                   self.time_offset)

        sliced_bp._time_resampled_to_trigger = self._time_resampled_to_trigger
        return sliced_bp

    def __eq__(self, other):
        """
        Return test of equality between two objects.

        Parameters
        ----------
        other:
            comparable object.

        Returns
        -------
        boolean
        """
        return are_equal(self, other)

    def rename_channels(self, new_names):
        """
        Rename the channels.

        If 'time' was specified, it makes sure that it's the first entry.

        Parameters
        ----------
        new_names: list of str
            New names for channels.

        Notes
        -----
        Outcome:
        self.ch_name: list of str
            Changes content to new_name.
        """
        if 'time' in new_names:
            del new_names[new_names.index('time')]

        new_names = ['time', ] + new_names

        self.ch_name = has_size(is_valid(new_names, list, list_type=str),
                                self.ch_amount, 'unknown')

    def return_index(self, idx):
        """
        Return the list entries of all the object properties, given an index.

        Parameters
        ----------
        idx: int
            Index of elements to return

        Returns
        -------
        out: tuple
            Tuple containing the proper list entry of all the
            properties of the object with index `idx`
        """
        return (self.timeseries[idx], self.ch_amount, self.freq[idx],
                self.ch_name[idx], self.units[idx])

    def delete_at_index(self, idx):
        """
        Delete the list entries of the object properties, given their index.

        Parameters
        ----------
        idx: int or range
            Index of elements to delete from all lists

        Notes
        -----
        Outcome:
        self.timeseries:
            Removes element at index idx
        self.freq:
            Removes element at index idx
        self.ch_name:
            Removes element at index idx
        self.units:
            Removes element at index idx
        self.trigger_idx:
            If the deleted index was the one of the trigger, set the trigger idx to 0.
        """
        del self.timeseries[idx]
        del self.freq[idx]
        del self.ch_name[idx]
        del self.units[idx]

        if self.trigger_idx == idx:
            LGR.warning('Removing trigger channel - are you sure you are doing'
                        'the right thing?')
            self.trigger_idx = 0

    def check_trigger_amount(self, thr=None, num_timepoints_expected=0, tr=0):
        """
        Count trigger points and correct time offset in channel "time".

        Parameters
        ----------
        thr: float
            Threshold to be used to detect trigger points.
            Default is 2.5
        num_timepoints_expected: int
            Number of expected triggers (num of TRs in fMRI)
        tr: float
            The Repetition Time of the fMRI data.

        Notes
        -----
        Outcome:
        self.thr: float
            Threshold used by the function to detect trigger points.
            If no threshold is provided, value is the mean of the trigger channel.
        self.num_timepoints_found: int
            Property of the `BlueprintInput` class.
            Contains the number of timepoints found
            with the automatic estimation.
        self.timeseries:
            The property `timeseries` is shifted with the 0 being
            the time of first trigger.
        """
        LGR.info('Counting trigger points')
        # Use the trigger channel to find the TRs,
        # comparing it to a given threshold.
        trigger = self.timeseries[self.trigger_idx]
        time = self.timeseries[0]
        LGR.info(f'The trigger is in channel {self.trigger_idx}')
        # Check that trigger and time channels have the same length.
        # If not, resample time to the length of the trigger
        if len(time) != len(trigger):
            LGR.warning('The trigger channel has a different sampling '
                        'from the registered time. Using a resampled version '
                        'of time to find the starting time.')
            time = np.linspace(time[0], time[-1], len(trigger))

            self._time_resampled_to_trigger = time

        flag = 0
        if thr is None:
            # If trigger channels are binary
            # (i.e., "on" is a higher value and "off" is a lower value)
            # and each "on" and "off" are each always approzimately the same value
            # then any value above the mean is "on" and every value below the mean
            # is "off".
            thr = np.mean(trigger)
            flag = 1
        timepoints = trigger > thr
        num_timepoints_found = len([is_true for is_true, _ in groupby(timepoints,
                                    lambda x: x != 0) if is_true])
        if flag == 1:
            LGR.info(f'The number of timepoints according to the std_thr method '
                     f'is {num_timepoints_found}. The computed threshold is {thr:.4f}')
        else:
            LGR.info(f'The number of timepoints found with the manual threshold of {thr:.4f} '
                     f'is {num_timepoints_found}')
        time_offset = time[timepoints.argmax()]

        if num_timepoints_expected:
            LGR.info('Checking number of timepoints')
            if num_timepoints_found > num_timepoints_expected:
                timepoints_extra = (num_timepoints_found
                                    - num_timepoints_expected)
                LGR.warning(f'Found {timepoints_extra} timepoints'
                            ' more than expected!\n'
                            'Assuming extra timepoints are at the end '
                            '(try again with a more liberal thr)')

            elif num_timepoints_found < num_timepoints_expected:
                timepoints_missing = (num_timepoints_expected
                                      - num_timepoints_found)
                LGR.warning(f'Found {timepoints_missing} timepoints'
                            ' less than expected!')
                if tr:
                    LGR.warning('Correcting time offset, assuming missing '
                                'timepoints are at the beginning (try again '
                                'with a more conservative thr)')
                    time_offset -= (timepoints_missing * tr)
                else:
                    LGR.warning('Can\'t correct time offset - you should '
                                'specify the TR')

            else:
                LGR.info('Found just the right amount of timepoints!')

        else:
            LGR.warning('The necessary options to find the amount of timepoints '
                        'were not provided.')
        self.thr = thr
        self.time_offset = time_offset
        self.timeseries[0] = self.timeseries[0] - time_offset
        self.num_timepoints_found = num_timepoints_found

    def print_info(self, filename):
        """
        Print info on the file, channel by channel.

        Parameters
        ----------
        filename: str or path
            Name of the input file to phys2bids

        Notes
        -----
        Outcome:
        ch:
            Returns to stdout (e.g. on screen) channels,
            their names and their sampling rate.
        """
        info = (f'\n------------------------------------------------'
                f'\nFile {filename} contains:\n')
        for ch in range(1, self.ch_amount):
            info = info + (f'{ch:02d}. {self.ch_name[ch]};'
                           f' sampled at {self.freq[ch]} Hz\n')
        info = info + '------------------------------------------------\n'

        LGR.info(info)

    def auto_trigger_selection(self):
        """
        Find a trigger index automatically.

        It compares the channel name with the the regular expressions stored
        in TRIGGER_NAMES. If that fails a time-domain recognition of the
        trigger signal is performed.

        Parameters
        ----------
        self

        Raises
        ------
        Exception
        More than one possible trigger channel was automatically found.

        Notes
        -----
        Outcome:
            trigger_idx : int
                Automatically retrieved trigger index
        """
        LGR.info('Running automatic trigger detection.')
        joint_match = '§'.join(TRIGGER_NAMES)
        indexes = []
        for n, case in enumerate(self.ch_name):
            name = re.split(r'(\W+|\d|_|\s)', case)
            name = list(filter(None, name))

            if re.search('|'.join(name), joint_match, re.IGNORECASE):
                indexes = indexes + [n]

        if indexes:
            if len(indexes) > 1:
                raise Exception('More than one possible trigger channel was automatically found. '
                                'Please run phys2bids specifying the -chtrig argument.')
            else:
                self.trigger_idx = indexes[0]
        else:
            # Time-domain automatic trigger detection

            # Create numpy array with all channels (excluding time)
            channel_ts = np.array(self.timeseries[1:])

            # Normalize each signal to [0,1]
            min_ts = np.min(channel_ts, axis=1)[:, None]
            max_ts = np.max(channel_ts, axis=1)[:, None]
            channel_ts = (channel_ts - min_ts) / (max_ts - min_ts)

            # Compute distance to the closest signal limit (0 or 1)
            distance = np.minimum(abs(channel_ts - 0), abs(channel_ts - 1))
            distance_mean = np.mean(distance, axis=1)

            # Set the trigger as the channel with the smallest distance
            self.trigger_idx = np.nanargmin(distance_mean) + 1

        LGR.info(f'{self.ch_name[self.trigger_idx]} selected as trigger channel')


class BlueprintOutput():
    """
    Main output object for phys2bids.

    Contains the blueprint to be exported.

    Attributes
    ----------
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
    filename : string
        Filename the object will be saved with. Init as empty string


    Methods
    -------
    ch_amount:
        Property. Returns number of channels (ch).
    return_index:
        Returns the proper list entry of all the
        properties of the object, given an index.
    delete_at_index:
        Returns all the proper list entry of the
        properties of the object, given an index.
    init_from_blueprint:
        method to populate from input blueprint instead of init
    """

    def __init__(self, timeseries, freq, ch_name, units, start_time, filename=''):
        """Initialise BlueprintOutput (see class docstring)."""
        self.timeseries = deepcopy(is_valid(timeseries, np.ndarray))
        self.freq = deepcopy(is_valid(freq, (int, float)))
        self.ch_name = deepcopy(has_size(ch_name, self.ch_amount, 'unknown'))
        self.units = deepcopy(has_size(units, self.ch_amount, '[]'))
        self.start_time = deepcopy(start_time)
        self.filename = deepcopy(is_valid(filename, str))

    @property
    def ch_amount(self):
        """
        Property. Returns number of channels (ch).

        Returns
        -------
        int
            Number of channels
        """
        return self.timeseries.shape[1]

    def __eq__(self, other):
        """
        Return test of equality between two objects.

        Parameters
        ----------
        other:
            comparable object.

        Returns
        -------
        boolean
        """
        return are_equal(self, other)

    def return_index(self, idx):
        """
        Return the list entries of all the object properties, given an index.

        Parameters
        ----------
        idx: int
            Index of elements to return

        Returns
        -------
        out: tuple
            Tuple containing the proper list entry of all the
            properties of the object with index `idx`
        """
        return (self.timeseries[:, idx], self.ch_amount, self.freq,
                self.ch_name[idx], self.units[idx], self.start_time)

    def delete_at_index(self, idx):
        """
        Delete the list entries of the object properties, given their index.

        Parameters
        ----------
        idx: int or range
            Index of elements to delete from all lists

        Notes
        -----
        Outcome:
        self.timeseries:
            Removes element at index idx
        self.ch_name:
            Removes element at index idx
        self.units:
            Removes element at index idx
        self.ch_amount:
            In all the property that are lists, the element correspondent to
            `idx` gets deleted
        """
        self.timeseries = np.delete(self.timeseries, idx, axis=1)
        del self.ch_name[idx]
        del self.units[idx]

    @classmethod
    def init_from_blueprint(cls, blueprint):
        """
        Populate the output blueprint using BlueprintInput.

        Parameters
        ----------
        cls: :obj: `BlueprintOutput`
            The object on which to operate
        blueprint: :obj: `BlueprintInput`
            The input blueprint object.
            !!! All its frequencies should be the same !!!

        Returns
        -------
        cls: :obj: `BlueprintOutput`
            Populated `BlueprintOutput` object.
        """
        timeseries = np.asarray(blueprint.timeseries).T
        freq = blueprint.freq[0]
        ch_name = blueprint.ch_name
        units = blueprint.units
        start_time = timeseries[0, 0]
        return cls(timeseries, freq, ch_name, units, start_time)
