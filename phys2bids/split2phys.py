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

    Runs the split parser, does some check on inputs and exports
    end indexes of each run based on npt_list and tr_list

    Arguments
    ---------

    Returns
    --------
        ...
    """

    # Initialize dictionaries to save phys_in endpoints
    run_timestamps = {}

    # initialise start index as 0
    start_index = 0

    for run_idx, run_tps in enumerate(ntp_list):
        # ascertain run length and initialise Blueprint object
        phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])

        # define padding - 20s * freq of trigger - padding is in nb of samples
        padding = 20 * phys_in.freq[chtrig]

        # LET'S START NOT SUPPORTING MULTIFREQ - end_index is nb of samples in run+start+first_trig
        end_index = run_tps * tr_list[run_idx] * phys_in.freq[chtrig] + \
            start_index + phys_in.trig_idx

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[chtrig].shape[0] < (end_index + padding):
            padding = phys_in.timeseries[chtrig].shape[0] - end_index

        # Save start: and end_index in dictionary
        # While saving, add the padding
        run_timestamps[run_idx] = (start_index, (end_index + padding))

        # set start_index for next run as end_index of this one
        start_index = end_index

        # phys_in.start_at_time(start_index)
        # NOTE : if we aim for updating indexes, how do we keep original timestamps ?

    # make dict exportable
    # or call it from phys2bids
    # or call phys2bids from here
    # or integrate this bit of code in phys2bids and adapt main parser by accepting
    # lists and adding -run argument
