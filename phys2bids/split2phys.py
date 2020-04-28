#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A parallel CLI utility to segment the physiological input files.

Cuts the physiological recording files into multiple runs
with padding at start and end

"""

from phys2bids.physio_obj.BlueprintInput import check_trigger_amount


def split2phys(phys_in=None, ntp_list=[0, ], tr_list=[1, ]):
    """
    Parallel workflow of phys2bids.



    Arguments
    ---------

    Returns
    --------
        ...
    """

    # Initialize dictionaries to save phys_in endpoints
    run_timestamps = {}

    for run_idx, run_tps in enumerate(ntp_list):

        # initialise Blueprint object with run info
        phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])

        # define padding - 20s * freq of trigger - padding is in nb of samples
        padding = 20 * phys_in.freq[0]

        # initialise start of run as index of first trigger (after padd of last run if not first)
        run_start = phys_in.trigger_idx

        # LET'S START NOT SUPPORTING MULTIFREQ - end_index is nb of samples in run+first_trig
        run_end = run_tps * tr_list[run_idx] * phys_in.freq[0] + phys_in.trigger_idx

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[0].shape[0] < (run_end + padding):
            padding = phys_in.timeseries[0].shape[0] - run_end

        # Save start: and end_index in dictionary
        # While saving, add the padding
        run_timestamps[run_idx] = ((run_start - padding), (run_end + padding))

        # update obj - SHOULD IT BE THE NEW START IDX OR A TUPLE (new_start,same_end )
        phys_in.__getitem__(run_end)
        # NOTE :  how do we keep original timestamps ?

    return(run_timestamps)
