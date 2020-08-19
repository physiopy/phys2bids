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

    # Convert data into 1d numpy array for easier indexing.
    data = np.squeeze(np.asarray(mat_dict['data']))

    # Extract number of channels.
    n_channels = len(mat_dict['titles'])

    # Stores MATLAB data into lists.
    timeseries = [data[:int(mat_dict['dataend'][0])], ]
    freq = [mat_dict['samplerate'][ch][0] for ch in range(n_channels)]
    units = [mat_dict['unittext'][int(mat_dict['unittextmap'][ch][0] - 1)].strip() for ch in range(n_channels)]
    names = [mat_dict['titles'][ch].strip() for ch in range(n_channels)]

    # Appends data from channels > 1.
    if n_channels > 1:
        for ch in range(n_channels - 1):
            idx_start = int(mat_dict['dataend'][ch]) + 1
            idx_end = int(mat_dict['dataend'][ch+1])
            timeseries.append(data[idx_start:idx_end])

    return BlueprintInput(timeseries, freq, names, units, chtrig)
