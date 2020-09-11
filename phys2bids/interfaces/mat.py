#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""phys2bids interface for MATLAB files."""

import logging

import numpy as np
from scipy.io import loadmat

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input from MATLAB files.

    Parameters
    ----------
    filename: str
        path to the txt labchart file
    chtrig : int
        index of trigger channel.
        !!! ATTENTION: IT'S MEANT TO REPRESENT AN INDEX STARTING FROM 1 !!!

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
    # Load MATLAB file into dictionary.
    mat_dict = loadmat(filename)

    breakpoint()
    # See if MATLAB is in ACQ format.
    if '__header__' in mat_dict:
        orig_names = mat_dict['labels']
        orig_units = mat_dict['units']
        interval = mat_dict['isi'][0][0]
        interval_units = mat_dict['isi_units'][0]
        data = mat_dict['data']

        timeseries = []
        freq = [t_freq, ]
        units = ['s', ]
        names = ['time', ]

        if 'Hz' in interval_units:
            print('frequency is given in the header, calculating sample Interval'
                ' and standarizing to Hz if needed')
            freq = float(interval)
            freq_unit = interval_units
            if freq_unit == 'MHz':
                freq = freq * (1000000)
            elif freq_unit == 'kHz':
                freq = freq * 1000
            interval = 1 / freq
            freq = [freq] * (len(timeseries) + 1)
        else:
            # check if interval is in seconds, if not change the units to seconds and
            # calculate frequency
            if interval_units != 'sec':
                LGR.warning('Interval is not in seconds. Converting its value.')
                if interval_units == 'min':
                    interval = float(interval) * 60
                    interval_units = 's'
                elif interval_units == 'msec':
                    interval = float(interval) / 1000
                    interval_units = 's'
                elif interval_units == 'µsec':
                    interval = float(interval) / 1000000
                    interval_units = 's'
            else:
                interval = float(interval)
                interval_units = 's'
            freq = [1 / interval] * (len(timeseries) + 1)
    else:
        # Convert data into 1d numpy array for easier indexing.
        data = np.squeeze(np.asarray(mat_dict['data']))

        # Extract number of channels and tick rate.
        n_channels = len(mat_dict['titles'])
        t_freq = mat_dict['tickrate'][0][0]

        # Stores MATLAB data into lists.
        timeseries = []
        freq = [t_freq, ]
        units = ['s', ]
        names = ['time', ]

        for ch in range(n_channels):
            units.append(mat_dict['unittext'][int(mat_dict['unittextmap'][ch][0] - 1)].strip())
            names.append(mat_dict['titles'][ch].strip())
            freq.append(mat_dict['samplerate'][ch][0])
            idx_start = int(mat_dict['datastart'][ch])
            idx_end = int(mat_dict['dataend'][ch])
            timeseries.append(data[idx_start:idx_end])

        # Calculate duration based on frequency and create time channel.
        interval = 1 / t_freq
        duration = (timeseries[0].shape[0] + 1) * interval
        t_ch = np.ogrid[0:duration:interval][:-1]
        timeseries = [t_ch, ] + timeseries

    return BlueprintInput(timeseries, freq, names, units, chtrig)
