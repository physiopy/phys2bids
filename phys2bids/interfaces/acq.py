#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""phys2bids interface for acqknowledge files."""
import logging
import warnings

from bioread import read_file

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def populate_phys_input(filename, chtrig):
    """
    Populate object phys_input from acq files.

    Parameters
    ----------
    filename: str
        path to the txt labchart file
    chtrig : int
        index of trigger channel

    Returns
    -------
    BlueprintInput

    See Also
    --------
    physio_obj.BlueprintInput
    """

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        data = read_file(filename).channels

    freq = [data[chtrig].samples_per_second, ]
    timeseries = [data[chtrig].time_index, ]
    units = ['s', ]
    names = ['time', ]

    for k, ch in enumerate(data):
        LGR.info(f'{k:02d}. {ch}')
        timeseries.append(ch.data)
        freq.append(ch.samples_per_second)
        units.append(ch.units)
        names.append(ch.name)

    return BlueprintInput(timeseries, freq, names, units, chtrig)
