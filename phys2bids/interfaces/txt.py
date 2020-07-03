#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""phys2bids interface for txt files."""

import logging
from collections import Counter
from operator import itemgetter

import numpy as np

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def check_multifreq(timeseries, freq, start=0, leftout=0):
    """
    Check if there are channels with different frequency than the maximum one.

    Parameters
    ----------
    timeseries: list
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


def process_labchart(channel_list, chtrig, header=[]):
    """
    Process labchart header and channel_list and make a physio_obj.BlueprintInput.

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
    # check header has some length
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    interval = header[0][1].split(" ")
    # check the interval is in some of the correct labchart units
    if interval[-1] not in ['hr', 'min', 's', 'ms', 'µs']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a valid LabChart'
                             'time unit, this probably means your file is not in Labchart format')
    # check if interval is in seconds, if not change the units to seconds
    if interval[-1] != 's':
        LGR.warning('Interval is not in seconds. Converting its value.')
        if interval[-1] == 'hr':
            interval[0] = float(interval[0]) * 3600
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
    units = ['s', ]
    # get names
    orig_names = header[4][1:]
    orig_names_len = len(orig_names)
    names = ['time', ]
    # get channels
    # this transposes the channel_list from a list of samples x channels to
    # a list of channels x samples
    timeseries = list(map(list, zip(*channel_list)))
    freq = [1 / interval[0]] * len(timeseries)
    timeseries = [np.array(darray) for darray in timeseries]
    # check the file has a time channel if not create it and add it
    # As the "time" doesn't have a column header, if the number of header names
    # is less than the number of timesieries, then "time" is column 0...
    # ...otherwise, create the time channel
    if not (orig_names_len < len(timeseries)):
        duration = (timeseries[0].shape[0] + 1) * interval[0]
        t_ch = np.ogrid[0:duration:interval[0]][:-1]  # create time channel
        timeseries = [t_ch, ] + timeseries
    names = names + orig_names
    units = units + orig_units
    freq = [1 / interval[0]] * len(timeseries)
    freq = check_multifreq(timeseries, freq)
    return BlueprintInput(timeseries, freq, names, units, chtrig + 1)


def process_acq(channel_list, chtrig, header=[]):
    """
    Process AcqKnowledge header and channel_list to make a physio_obj.BlueprintInput.

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
        If sampling is not in ['min', 'sec', 'µsec', 'msec','MHz', 'kHz', 'Hz'] reference:
        https://www.biopac.com/wp-content/uploads/acqknowledge_software_guide.pdf page 194

    See Also
    --------
    physio_obj.BlueprintInput
    """
    # check header is not empty
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    header.append(channel_list[0])
    del channel_list[0]  # delete sample size from channel list
    # this transposes the channel_list from a list of samples x channels to
    # a list of channels x samples
    timeseries = list(map(list, zip(*channel_list)))

    interval = header[1][0].split()
    # check the interval is in some of the correct AcqKnowledge units
    if interval[-1].split('/')[0] not in ['min', 'sec', 'µsec', 'msec', 'MHz', 'kHz', 'Hz']:
        raise AttributeError(f'Interval unit "{interval[-1]}" is not in a '
                             'valid AcqKnowledge format time unit, this probably'
                             'means your file is not in min, sec, msec, µsec, Mhz, KHz or Hz')
    interval[-1] = interval[-1].split('/')[0]
    # Check if the header is in frequency or sampling interval
    if 'Hz' in interval[-1].split('/')[0]:
        print('frequency is given in the header, calculating sample Interval'
              ' and standarizing to Hz if needed')
        freq = float(interval[0])
        freq_unit = interval[-1]
        if freq_unit == 'MHz':
            freq = freq * (1000000)
        elif freq_unit == 'kHz':
            freq = freq * 1000
        interval[0] = 1 / freq
        freq = [freq] * (len(timeseries) + 1)
    else:
        # check if interval is in seconds, if not change the units to seconds and
        # calculate frequency
        if interval[-1].split('/')[0] != 'sec':
            LGR.warning('Interval is not in seconds. Converting its value.')
            if interval[-1].split('/')[0] == 'min':
                interval[0] = float(interval[0]) * 60
                interval[-1] = 's'
            elif interval[-1].split('/')[0] == 'msec':
                interval[0] = float(interval[0]) / 1000
                interval[-1] = 's'
            elif interval[-1].split('/')[0] == 'µsec':
                interval[0] = float(interval[0]) / 1000000
                interval[-1] = 's'
        else:
            interval[0] = float(interval[0])
            interval[-1] = 's'
        freq = [1 / interval[0]] * (len(timeseries) + 1)
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
    names = ['time', ]
    names = names + orig_names
    # reoder channels units
    units = ['s', ]
    units = units + orig_units
    # get channels
    timeseries = [np.array(darray) for darray in timeseries]
    duration = (timeseries[0].shape[0] + 1) * interval[0]
    t_ch = np.ogrid[0:duration:interval[0]][:-1]  # create time channel
    timeseries = [t_ch, ] + timeseries
    freq = check_multifreq(timeseries, freq)
    return BlueprintInput(timeseries, freq, names, units, chtrig + 1)


def read_header_and_channels(filename, chtrig):
    """
    Read a txt file with a header and channels and separate them.

    Parameters
    ----------
    filename: str
        path to the txt Labchart file
    chtrig : int
        index of trigger channel

    Returns
    -------
    header: list
        header lines
    channel_list:list
        channel lines in list

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

    See Also
    --------
    physio_obj.BlueprintInput
    """
    chtrig = chtrig - 1  # now for the user channel indexing starts at 1 as it
    # happens in acq call
    header, channel_list = read_header_and_channels(filename, chtrig)
    # check header is not empty and detect if it is in labchart or Acqknoledge format
    if len(header) == 0:
        raise AttributeError('Files without header are not supported yet')
    elif 'Interval=' in header[0]:
        LGR.info('phys2bids detected that your file is in Labchart format')
        phys_in = process_labchart(channel_list, chtrig, header)
    elif 'acq' in header[0][0]:
        LGR.info('phys2bids detected that your file is in AcqKnowledge format')
        phys_in = process_acq(channel_list, chtrig, header)
    else:
        raise AttributeError('This file format is not supported yet for txt files')
    return phys_in
