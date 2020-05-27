#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import where


def find_run_timestamps(phys_in, ntp_list, tr_list, padding=9):
    """
    Find beginning and ending of each "run" in a multirun recording.

    Returns dictionary key for each run in BlueprintInput object based on user's entries
    Each key has a tuple expressing the timestamps of run in nb of samples(based on trigger chan)
    Timestamps are the index of first and last triggers of a run, adjusted with padding
    run_start and run_end indexes refer to the samples contained in the whole session

    Parameters
    ---------
    phys_in : object
        Object returned by BlueprintInput class
    ntp_list : list
        a list of integers given by the user as `ntp` input
        Default: [0, ]
    tr_list : list
        a list of float given by the user as `tr` input
        Default: [1,]
    Returns
    --------
    run_timestamps : dictionary of tuples
        Containing tuples of run start and end indexes for each run, based on trigger channels
        In the form of run_timestamps{run_idx:(start, end), run_idx:...}
    """
    # Initialize dictionaries to save phys_in slices
    run_timestamps = {}
    # run_start = 0

    # define padding - 9s * freq of trigger - padding is in nb of samples
    padding = padding * phys_in.freq[0]

    for run_idx, run_tps in enumerate(ntp_list):

        # (re)initialise Blueprint object with current run info - correct time offset
        phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])

        # initialise start of run as index of first trigger minus the padding
        # the first trigger is always at 0 seconds
        run_start = where(phys_in.timeseries[0] == 0) - padding

        # run length in seconds
        end_sec = (run_tps * tr_list[run_idx])

        # define index of the run's last trigger
        # run_end = find index of phys_in.timeseries[0] > end_sec
        run_end = where(phys_in.timeseries[0] > end_sec)

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[0].shape[0] < (run_end + padding):
            padding = phys_in.timeseries[0].shape[0] - run_end

        # update the object so that it will look for the first trigger after previous run end
        phys_in = phys_in[(run_end + 1):]

        # Save start and end_index in dictionary
        # keep original timestamps by adjusting the indexes with previous end_index
        # While saving, add the padding for end index
        if run_idx > 0:
            previous_end_index = run_timestamps[run_idx - 1][1]
            run_start = run_start + previous_end_index
            run_end = run_end + previous_end_index

        run_timestamps[run_idx] = (run_start, run_end + padding)

    return run_timestamps


def split4phys(phys_in, ntp_list, tr_list, padding=9):
    """
    Split runs for phys2bids.

    Returns a dictionary containing one BlueprintInput per run.

    Parameters
    ---------
    phys_in : object
        Object returned by BlueprintInput class
    ntp_list : list
        a list of integers given by the user as `ntp` input
        Default: [0, ]
    tr_list : list
        a list of float given by the user as `tr` input
        Default: [1,]
    Returns
    --------
    phys_in: dictionary of BlueprintInput objects
        Containing tuples of run start and end indexes for each run, based on trigger channels
        In the form of run_timestamps{run_idx:(start, end), run_idx:...}

    """
    run_timestamps = find_run_timestamps(phys_in, ntp_list, tr_list, padding=9)

    # do stuff

    return phys_in
