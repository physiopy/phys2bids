#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import where
import logging

LGR = logging.getLogger(__name__)


def find_runs(phys_in, ntp_list, tr_list, thr=None, padding=9):
    """
    Find runs slicing index.

    Returns dictionary key for each run in BlueprintInput object based on
    user's entries. Each key has a tuple of 4 elements, 2 expressing the
    timestamps of run in nb of samples. Timestamps are the index of first and
    last triggers of a run, adjusted with padding. run_start and run_end
    indexes refer to the samples contained in the whole session.
    First trigger time offset and nb of triggers contained in the run are also indicated.

    Parameters
    ---------
    phys_in: BlueprintInput object
        Object returned by BlueprintInput class
    ntp_list: list
        a list of integers given by the user as `ntp` input
    tr_list: list
        a list of float given by the user as `tr` input
    thr: int
        inherit threshold for detection of trigger given by user
    padding: int
        extra time at beginning and end of timeseries, expressed in seconds (s)
        Default: 9

    Returns
    --------
    run_timestamps: dictionary
        Containing tuples of run start and end indexes for each run, based on
        trigger channels. It also contains run attributes: time offset from
        session beggining, and nb of triggers in the form of
        run_timestamps{1:(start, end, time offset, nb of triggers),
                       2:(...), ... }
    """
    # Initialize dictionaries to save  run timestamps and phys_in attributes
    run_timestamps = {}

    # Express the padding in samples equivalent
    padding = padding * phys_in.freq[0]

    # enumerate user input  num_timepoints_expected
    for run_idx, run_tps in enumerate(ntp_list):

        # correct time offset for this iteration's object
        phys_in.check_trigger_amount(thr=thr, num_timepoints_expected=run_tps, tr=tr_list[run_idx])

        # If it's the very first run, start the run at sample 0,
        # otherwise "add" the padding
        if run_idx == 0:
            run_start = 0
        else:
            run_start = where(phys_in.timeseries[0] <= 0)[0][0] - padding

        # Defining end of acquisition
        # run length in seconds
        end_sec = run_tps * tr_list[run_idx]

        # define index of the run's last trigger + padding (HAS TO BE INT type)
        # pick first value of time array that is over specified run length
        # where returns list of values over end_sec and its dtype, choose [list][first value]
        run_end = int(where(phys_in.timeseries[0] > end_sec)[0][0] + padding)
        update = int(run_end - padding + 1)

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[0].shape[0] < run_end:
            run_end = phys_in.timeseries[0].shape[0]

        # Adjust timestamps with previous end_index
        # Except if it's the first run
        if run_idx > 0:
            previous_end_index = run_timestamps[run_idx][1]
            # adjust time_offset to keep original timing information
            phys_in.time_offset = phys_in.time_offset + run_timestamps[run_idx][2]
            run_start = int(run_start + previous_end_index)
            run_end = int(run_end + previous_end_index)

        # Save *start* and *end_index* in dictionary along with *time_offset* and *ntp found*
        # dict key must be readable by human
        # LGRinfo
        LGR.info("\n--------------------------------------------------------------\n"
                 f"Slicing between {(run_start/phys_in.freq[phys_in.trigger_idx])} seconds and "
                 f"{run_end/phys_in.freq[phys_in.trigger_idx]} seconds\n"
                 "--------------------------------------------------------------")

        run_timestamps[run_idx + 1] = (run_start, run_end,
                                       phys_in.time_offset,
                                       phys_in.num_timepoints_found)

        # update the object so that next iteration will look for the first trigger
        # after previous run's last trigger. maybe padding extends to next run
        phys_in = phys_in[update:-1]

    return run_timestamps


def slice4phys(phys_in, ntp_list, tr_list, padding=9):
    """
    Slice runs for phys2bids.

    Parameters
    ---------
    phys_in: BlueprintInput object
        Object returned by BlueprintInput class
    ntp_list: list
        a list of integers given by the user as `ntp` input
        Default: [0, ]
    tr_list: list
        a list of float given by the user as `tr` input
        Default: [1,]
    padding: int
        extra time at beginning and end of timeseries, expressed in seconds (s)
        Default: 9

    Returns
    --------
    phys_in_slices: dict
        keys start by `run 1` until last (`run n`).
        items are slices of BlueprintInput objects based on run attributes returned by
        internal function (`slice4phys` takes the same arguments as `find_runs`)
    """
    phys_in_slices = {}
    # inform the user
    LGR.warning("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                "\nphys2bids will split the input file according to the given -tr and -ntp"
                " arguments"
                "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Find the timestamps
    run_timestamps = find_runs(phys_in, ntp_list, tr_list, padding)

    for run in run_timestamps.keys():

        # tmp variable to collect run's info
        run_attributes = run_timestamps[run]

        phys_in_slices[run] = phys_in[run_attributes[0]:run_attributes[1]]

        # Overwrite current run phys_in attributes
        # 3rd item of run_attributes is adjusted time offset
        phys_in_slices[run].time_offset = run_attributes[2]
        # 4th item of run_attributes is the nb of tp found by check_trigger_amount
        phys_in_slices[run].num_timepoints_found = run_attributes[3]

    return phys_in_slices
