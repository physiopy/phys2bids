#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""phys2bids interface for acqknowledge files."""
import logging
import warnings

from bioread import read_file

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def populate_phys_input(filename, chtrig=0):
    """
    Populate object phys_input from acq files.

    Parameters
    ----------
    filename: str
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
