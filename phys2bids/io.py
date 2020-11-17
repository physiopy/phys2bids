#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""phys2bids interfaces for txt  and acq extension files."""

import logging
from collections import Counter
import numpy as np
from operator import itemgetter
import warnings

from bioread import read_file

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def check_multifreq(timeseries, freq, start=0, leftout=0):
    """
    Check if there are channels with different frequency than the maximum one.

    Parameters
    ----------
    timeseries : list of arrays
        list with channels only in np array format
    freq : list
        list with the maximun frequency
    start : integer
        first sample of the channel to be considered
    leftout : integer
        number of samples at the end of the channel that are not considered
        This is done  so this process doesn't take forever

    Returns
    -------
    mfreq: list
        new list with the actual frequency of the channels
    """
    mfreq = []
    # for each channel check frequency
    max_equal = 1
    for idx, chann in enumerate(timeseries):
        eq_list = []
        # cut the beggining of the channel
        chann = chann[start:]
        while len(chann) > max_equal:
            eq_samples = 1  # start counter
            for idx2, value in enumerate(chann[1:]):
                # if value equal to previous value
                if value == chann[idx2]:
                    # count number of identic samples
                    eq_samples += 1
                else:
                    # save this number when the next sample is not equal
                    eq_list.append(eq_samples)
                    # remove the samples that where equal
                    chann = chann[idx2 + 1:]
                    if max_equal < eq_samples:
                        max_equal = eq_samples
                    break
        # count the number of ocurrences in eq_list
        dict_fr = Counter(eq_list)
        # get maximum
        n_inter_samples = max(dict_fr.items(), key=itemgetter(1))[0]
        # if there are interpolated samples, it means the frequency is lower
        # decrease frequency by dividing for the number of interpolated samples
        mfreq.append(freq[idx] / n_inter_samples)
    return mfreq


def process_blueprint_items(channel_list, chtrig, interval, orig_units, orig_names):
    """
    Process items header items and channel_list and make a physio_obj.BlueprintInput.

    Parameters
    ----------
    channel_list : list of strings
        list with channels only
    chtrig : int
        index of trigger channel, starting in 1 for human readability
    interval : list of strings
        maximum sampling frequency or interval value and unit for the recording
    orig_units : list of strings
        contains original channels units
    orig_names : list of strings
        contains original channels name

    Returns
    -------
    BlueprintInput

    Raises
    ------
    ValueError
        If len(header) == 0 and therefore there is no header
        If sampling is not in ['min', 'sec', 'µsec', 'msec', 'MHz', 'kHz', 'Hz', 'hr', 'min', 's',
        'ms', 'µs'] reference:
        https://www.adinstruments.com/support/knowledge-base/how-can-channel-titles-ranges-intervals-etc-text-file-be-imported-labchart
        https://www.biopac.com/wp-content/uploads/acqknowledge_software_guide.pdf page 194

    See Also
    --------
    physio_obj.BlueprintInput
    """
    # this transposes the channel_list from a list of samples x channels to
    # a list of channels x samples
    timeseries = list(map(list, zip(*channel_list)))
    if interval[-1] not in ['min', 'sec', 'µsec', 'msec', 'MHz', 'kHz', 'Hz', 'hr', 'min', 's',
                            'ms', 'µs']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a '
                             'valid frequency or time unit format, this probably'
                             'means your file is not in min, sec, msec, µsec, hr, min, s, ms, µs,'
                             'Mhz, KHz or Hz')
    # Check if the header is in frequency or sampling interval
    if 'Hz' in interval[-1]:
        print('frequency is given in the header, calculating sample Interval'
              ' and standarizing to Hz if needed')
        freq = float(interval[0])
        freq_unit = interval[-1]
        if freq_unit == 'MHz':
            freq = freq * (1000000)
        elif freq_unit == 'kHz':
            freq = freq * 1000
        interval[0] = 1 / freq
        freq = [freq] * len(timeseries)
    else:
        # check if interval is in seconds, if not change the units to seconds and
        # calculate frequency
        if interval[-1] != 's':
            LGR.warning('Interval is not in seconds. Converting its value and unit.')
            if interval[-1] == 'min':
                interval[0] = float(interval[0]) * 60
                interval[-1] = 's'
            elif interval[-1] == 'msec':
                interval[0] = float(interval[0]) / 1000
                interval[-1] = 's'
            elif interval[-1] == 'µsec':
                interval[0] = float(interval[0]) / 1000000
                interval[-1] = 's'
            if interval[-1] == 'hr':
                interval[0] = float(interval[0]) * 3600
                interval[-1] = 's'
            elif interval[-1] == 'ms':
                interval[0] = float(interval[0]) / 1000
                interval[-1] = 's'
            elif interval[-1] == 'µs':
                interval[0] = float(interval[0]) / 1000000
                interval[-1] = 's'
            elif interval[-1] == 'sec':
                interval[0] = float(interval[0])
                interval[-1] = 's'
        else:
            interval[0] = float(interval[0])
        # get frequency
        freq = [1 / interval[0]] * len(timeseries)
    # reorder channels names
    names = ['time', ]
    names = names + orig_names
    # reoder channels units
    units = ['s', ]
    units = units + orig_units
    timeseries = list(map(list, zip(*channel_list)))
    freq = [1 / interval[0]] * len(timeseries)
    timeseries = [np.array(darray) for darray in timeseries]
    # check the file has a time channel if not create it and add it
    # As the "time" doesn't have a column header, if the number of header names
    # is less than the number of timesieries, then "time" is column 0...
    # ...otherwise, create the time channel
    if not (len(orig_names) < len(timeseries)):
        duration = (timeseries[0].shape[0] + 1) * interval[0]
        t_ch = np.ogrid[0:duration:interval[0]][:-1]  # create time channel
        timeseries = [t_ch, ] + timeseries
        freq = [max(freq)] + freq
    freq = check_multifreq(timeseries, freq)
    return BlueprintInput(timeseries, freq, names, units, chtrig)


def read_header_and_channels(filename):
    """
    Read a txt file with a header and channels and separate them.

    Parameters
    ----------
    filename : str
        path to the txt Labchart file

    Returns
    -------
    header : list of strings
        header lines
    channel_list : list of strings
        The channels of the recording

    """
    header = []
    channel_list = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n').split('\t')
            while line[-1] == '':
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
    return header, channel_list


def extract_header_items(channel_list, header=[]):
    """
    Process items header and channel_list depending on the format (acqKnowledge and labchart).

    Parameters
    ----------
    channel_list : list of strings
        The channels of the recording
    header: list
        list that contains file header

    Returns
    -------
    interval : list of strings
        maximun sampling frequency or interval value and unit for the recording
    orig_units : list of strings
        contains original channels units
    orig_names : list of strings
        contains original channels name

    Raises
    ------
    ValueError
        If len(header) == 0 and therefore there is no header
        If files are not in acq or txt format
    """
    # check header is not empty and detect if it is in labchart or Acqknoledge format
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    elif 'Interval=' in header[0]:
        LGR.info('phys2bids detected that your file is in Labchart format')
        interval = header[0][1].split(" ")
        range_list = header[5][1:]
        orig_units = []
        for item in range_list:
            orig_units.append(item.split(' ')[1])
        orig_names = header[4][1:]
    elif 'acq' in header[0][0]:
        LGR.info('phys2bids detected that your file is in AcqKnowledge format')
        header.append(channel_list[0])
        del channel_list[0]  # delete sample size from channel list
        interval = header[1][0].split()
        interval[-1] = interval[-1].split('/')[0]
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
    else:
        raise AttributeError('This file format is not supported yet for txt files')
    return interval, orig_units, orig_names


def load_txt_ext(filename, chtrig=0):
    """
    Read .txt file into a BlueprintInput object.

    Parameters
    ----------
    filename : str
        path to the txt Labchart file
    chtrig : int
        index of trigger channel, starting in 1 for human readability

    Returns
    -------
    phys_in

    Raises
    ------
    ValueError
        If len(header) == 0 and therefore there is no header
        If files are not in acq or txt format

    See Also
    --------
    physio_obj.BlueprintInput
    """
    header, channel_list = read_header_and_channels(filename)
    interval, orig_units, orig_names = extract_header_items(channel_list, header)
    phys_in = process_blueprint_items(channel_list, chtrig, interval, orig_units, orig_names)
    return phys_in


def load_acq_ext(filename, chtrig=0):
    """
    Populate object phys_input from acq extension files.

    Parameters
    ----------
    filename : str
        path to the txt labchart file
    chtrig : int, optional
          index of trigger channel. Default is 0.

    Returns
    -------
    BlueprintInput

    Note
    ----
    chtrig is not a 0-based Python index - instead, it's human readable (i.e., 1-based).
    This is handy because, when initialising the class, a new channel corresponding
    to time is added at the beginning - that is already taken into account!

    See Also
    --------
    physio_obj.BlueprintInput
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        data = read_file(filename).channels

    freq = [data[0].samples_per_second, ]
    timeseries = [data[0].time_index, ]
    units = ['s', ]
    names = ['time', ]

    for k, ch in enumerate(data):
        LGR.info(f'{k:02d}. {ch}')
        timeseries.append(ch.data)
        freq.append(ch.samples_per_second)
        units.append(ch.units)
        names.append(ch.name)

    return BlueprintInput(timeseries, freq, names, units, chtrig)