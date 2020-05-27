#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import where


def find_run_timestamps(phys_in, ntp_list, tr_list, padding=9):
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
    # Initialize dictionaries to save phys_in slices
    run_timestamps = {}
    # run_start = 0

    # define padding - 9s * freq of trigger - padding is in nb of samples
    padding = padding * phys_in.freq[0]

    for run_idx, run_tps in enumerate(ntp_list):
        # Make run_idx human friendly :)
        run_idx += 1

        # (re)initialise Blueprint object with current run info - correct time offset
        phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])

        # initialise start of run as index of first trigger minus the padding
        # the first trigger is always at 0 seconds

        ### CHECK THAT YOU HAVE ENOUGH PADDING AT THE BEGINNING
        ### REMEMBER NOT TO OVERWRITE padding
        run_start = where(phys_in.timeseries[0] == 0) - padding

        # run length in seconds
        end_sec = (run_tps * tr_list[run_idx])

        # define index of the run's last trigger
        # run_end = find index of phys_in.timeseries[0] > end_sec
        run_end = where(phys_in.timeseries[0] > end_sec)

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        ### NOW THIS IS NOT OPTIMAL ANYMORE SINCE IT OVERWRITES padding
        ### BETTER TO CHANGE run_end HERE!!!
        if phys_in.timeseries[0].shape[0] < (run_end + padding):
            padding = phys_in.timeseries[0].shape[0] - run_end

        # Save start and end_index in dictionary
        # keep original timestamps by adjusting the indexes with previous end_index
        # Except if it's the first run
        # While saving, add the padding for end index
        if run_idx > 1:
            previous_end_index = run_timestamps[run_idx - 1][1]
            phys_in.time_offset = phys_in.time_offset + run_timestamps[run_idx - 1][2]
            run_start = run_start + previous_end_index
            run_end = run_end + previous_end_index

        ### TUPLE BECOMES FOUR ITEMS, THE LAST ARE related to check_trigger_amount
        run_timestamps[run_idx] = (run_start, run_end, phys_in.time_offset, phys_in.num_timepoints_found)

        # update the object so that it will look for the first trigger after previous run end
        phys_in = phys_in[(run_end + 1):]

<<<<<<< HEAD
    return run_timestamps


def split4phys(phys_in, ntp_list, tr_list, padding=9):
    """
    """
    multiphys_in = {}

    # Find the timestamps
    run_timestamps = find_run_timestamps(phys_in, ntp_list, tr_list, padding=9)

    for run in run_timestamps.keys():
        # Read the run_timestamps[run]

        # add item to multiphys_in that contains a slice of phys_in accordingly
        # The key of the item is "run"

        # Overwrite attributes phys_in.time_offset and phys_in.num_timepoints_found with the ones in the tuple (item 2 and 3)

    # return a dictionary that contains the sliced object
    # the key will be the internal run
    return multiphys_in

=======
    return multiphys_in
>>>>>>> sangfrois/split_utility
