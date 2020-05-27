#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import where


def find_runs(phys_in, ntp_list, tr_list, padding=9):
    """
    Split runs for phys2bids.

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
    run_timestamps : dictionary
        Containing tuples of run start and end indexes for each run, based on trigger channels
        In the form of run_timestamps{run_idx:(start, end), run_idx:...}
    call an internal function and feed it the dictionary instead
    """
    # Initialize dictionaries to save  run timestamps and phys_in's attributes
    run_timestamps = {}

    # define padding - default : 9s * freq of trigger
    padding = padding * phys_in.freq[0]

    # enumerate user input  num_timepoints_expected
    for run_idx, run_tps in enumerate(ntp_list):

        # (re)initialise Blueprint object with current run info - correct time offset
        phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])

        # Defining beginning of acquisition
        # if -9 s' index doesn't exist, start at beginning
        if where(phys_in.timeseries[0] == -9)[0].size < 1:  # where returns a tuple
            # the first trigger is always at 0 s
            run_start = where(phys_in.timeseries[0] == 0)
        else:
            # initialise start of run as index of first trigger minus the padding
            run_start = where(phys_in.timeseries[0] == 0) - padding

        # Defining end of acquisition
        # run length in seconds
        end_sec = (run_tps * tr_list[run_idx])

        # define index of the run's last trigger + padding
        run_end = where(phys_in.timeseries[0] > end_sec) + padding

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[0].shape[0] < run_end:
            run_end = phys_in.timeseries[0].shape[0]

        # Adjust timestamps with previous end_index
        # Except if it's the first run
        if run_idx > 1:
            previous_end_index = run_timestamps[run_idx - 1][1]
            # adjust time_offset to keep original timing information
            phys_in.time_offset = phys_in.time_offset + run_timestamps[run_idx - 1][2]
            run_start = run_start + previous_end_index
            run_end = run_end + previous_end_index

        # Save *start* and *end_index* in dictionary along with *time_offset* and *ntp found*
        # dict key must be readable
        run_timestamps["Run {}".format(run_idx + 1)] = (run_start, run_end,
                                                        phys_in.time_offset,
                                                        phys_in.num_timepoints_found)

        # update the object so that it will look for the first trigger after previous run end
        phys_in = phys_in[(run_end):]

    return run_timestamps


def slice4phys(phys_in, ntp_list, tr_list, padding=9):
    """
    """
    phys_in_slices = {}

    # Find the timestamps
    run_timestamps = find_runs(phys_in, ntp_list, tr_list, padding=9)

    for run in run_timestamps.keys():

        # tmp variable to collect run's info
        run_attributes = run_timestamps[run]

        run_obj = phys_in[run_attributes[0]:run_attributes[1]]

        run_

        # add item to multiphys_in that contains a slice of phys_in accordingly
        # The key of the item is "run"
        phys_in_slices[run] =

        # Overwrite attributes phys_in.time_offset and phys_in.num_timepoints_found with the ones in the tuple (item 2 and 3)

    # return a dictionary that contains the sliced object
    # the key will be the internal run
    return multiphys_in
