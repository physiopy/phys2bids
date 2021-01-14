"""Multi-run slicer for phys2bids package."""

import logging
from copy import deepcopy

import numpy as np

from phys2bids.bids import update_bids_name

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
        phys_in.check_trigger_amount(thr=thr, num_timepoints_expected=run_tps,
                                     tr=tr_list[run_idx])
        # If it's the very first run, start the run at sample 0,
        # otherwise start is first trigger (adjust with padding later)
        if run_idx == 0:
            run_start = 0
        else:
            run_start = int(np.where(np.isclose(phys_in.timeseries[0], 0))[0])

        # Defining end of acquisition
        # run length in seconds
        end_sec = run_tps * tr_list[run_idx]

        # define index of the run's last trigger + padding (HAS TO BE INT type)
        # pick first value of time array that is over specified run length
        # where returns list of values over end_sec and its dtype, choose [list][first value]
        run_end = int(np.where(phys_in.timeseries[0] > end_sec)[0][0] + padding)
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
            # update run_start, removing 2 paddings (one for this run, one for the previous)
            run_start = int(run_start + previous_end_index - 2 * padding)
            # update run_end, removing the padding of the previous end
            run_end = int(run_end + previous_end_index - padding)

        # Save *start* and *end_index* in dictionary along with *time_offset* and *ntp found*
        # dict key must be readable by human
        # LGRinfo
        LGR.info('\n--------------------------------------------------------------\n'
                 f'Slicing between {(run_start/phys_in.freq[phys_in.trigger_idx])} seconds and '
                 f'{run_end/phys_in.freq[phys_in.trigger_idx]} seconds\n'
                 '--------------------------------------------------------------')

        run_timestamps[run_idx + 1] = (run_start, run_end,
                                       phys_in.time_offset,
                                       phys_in.num_timepoints_found)

        # update the object so that next iteration will look for the first trigger
        # after previous run's last trigger. maybe padding extends to next run
        phys_in = deepcopy(phys_in[update:-1])

    return run_timestamps


def slice_phys(phys, run_timestamps, padding=9, update_trigger=False):
    """Slice a physio object based on run-/file-wise onsets and offsets.

    Parameters
    ----------
    phys : BlueprintInput
        Multi-run physio data in BlueprintInput object.
    run_timestamps : dict
        Each key is a run-wise filename and value is a tuple of (onset, offset),
        where onset and offset are integers corresponding to index values of
        the trigger channel.
    padding : float or tuple, optional
        Amount of time before and after run to keep in physio time series, in seconds.
        May be a single value (in which case the time before and after is the same) or
        a two-item tuple (which case the first item is time before and the second is
        time after).
        These values will be automatically reduced in cases where the pad would extend
        before or after the physio acquisition.
    update_trigger : bool, optional
        Whether to update the trigger channel time series based on estimated scan onsets from
        the BIDS dataset (True) or to leave it as-is (False). Default is False.

    Returns
    -------
    phys_in_slices : dict
        Each key is a run-wise filename (possibly further split by frequency)
        and each value is a BlueprintInput object.

    Notes
    -----
    The goal of this function is to abstract out the general slicing procedure
    from slice4phys.
    """
    phys = deepcopy(phys)
    if update_trigger:
        LGR.warning(
            "Overwriting the trigger channel. The original signal will be retained in a 'original trigger' channel."
        )
        phys.freq.append(phys.freq[phys.trigger_idx])
        phys.units.append(phys.units[phys.trigger_idx])
        phys.timeseries.append(phys.timeseries[phys.trigger_idx].copy())
        phys.ch_name.append("original trigger")

        # Fix up the trigger time series
        phys.timeseries[phys.trigger_idx][:] = 0
        for ons, off in run_timestamps.values():
            phys.timeseries[phys.trigger_idx][ons:off] = 1

    if not isinstance(padding, tuple):
        time_before, time_after = padding, padding
    else:
        time_before, time_after = padding

    phys_in_slices = {}
    for i_run, fname in enumerate(run_timestamps.keys()):
        run_attributes = run_timestamps[fname]  # tmp variable to collect run's info
        trigger_onset, trigger_offset = run_attributes
        min_onset, max_offset = 0, phys.timeseries[phys.trigger_idx].shape[0]

        unique_frequencies = np.unique(phys.freq)
        trigger_freq = phys.freq[phys.trigger_idx]

        # Limit padding based on beginning and end of physio recording.
        # We could also limit padding to prevent overlap between scans, if desired.
        run_time_before = np.minimum(
            time_before, (trigger_onset - min_onset) / trigger_freq
        )
        run_time_after = np.minimum(
            time_after, (max_offset - trigger_offset) / trigger_freq
        )

        for freq in unique_frequencies:
            to_subtract = int(run_time_before * freq)
            to_add = int(run_time_after * freq)

            run_onset_idx = int(trigger_onset * freq / trigger_freq) - to_subtract
            run_offset_idx = int(trigger_offset * freq / trigger_freq) + to_add

            # Split into frequency-specific object limited to onset-offset
            temp_phys_in = deepcopy(phys[run_onset_idx:run_offset_idx])

            if temp_phys_in.freq[temp_phys_in.trigger_idx] != freq:
                example_ts = phys.timeseries[phys.freq.index(freq)]

                # Determine time
                new_time = (
                    np.arange(example_ts.shape[0])
                    / temp_phys_in.timeseries[phys.freq.index(freq)].freq
                )
                new_time += np.min(temp_phys_in.timeseries[0])
                temp_phys_in.timeseries[0] = new_time
                temp_phys_in.freq[0] = freq

                # Resample trigger
                trigger = temp_phys_in.timeseries[temp_phys_in.trigger_idx]
                cur_xvals = np.arange(len(trigger))
                new_xvals = np.linspace(0, len(trigger), example_ts.shape[0])
                new_trigger = np.interp(
                    new_xvals,
                    cur_xvals,
                    temp_phys_in.timeseries[temp_phys_in.trigger_idx],
                )
                temp_phys_in.timeseries[temp_phys_in.trigger_idx] = new_trigger
                temp_phys_in.freq[temp_phys_in.trigger_idx] = freq

            if len(unique_frequencies) > 1:
                run_fname = update_bids_name(fname, recording=str(freq) + "Hz")

                # Drop other frequency channels
                channel_idx = np.arange(temp_phys_in.ch_amount)
                nonfreq_channels = [
                    i for i in channel_idx if temp_phys_in.freq[i] != freq
                ]
                freq_channels = [i for i in channel_idx if temp_phys_in.freq[i] == freq]
                temp_phys_in = temp_phys_in.delete_at_index(nonfreq_channels)

                # Update trigger channel index around dropped channels
                new_trigger_idx = freq_channels.index(temp_phys_in.trigger_idx)
                temp_phys_in.trigger_idx = new_trigger_idx
            else:
                run_fname = fname

            # zero out time
            temp_phys_in.timeseries[0] = temp_phys_in.timeseries[0] - np.min(
                temp_phys_in.timeseries[0]
            )
            # Now take out the time before the scan starts
            temp_phys_in.timeseries[0] = temp_phys_in.timeseries[0] - time_before

            phys_in_slices[run_fname] = temp_phys_in
    return phys_in_slices


def slice4phys(phys_in, ntp_list, tr_list, thr, padding=9):
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
    LGR.warning('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                '\nphys2bids will split the input file according to the given -tr and -ntp'
                ' arguments'
                '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Find the timestamps
    run_timestamps = find_runs(phys_in, ntp_list, tr_list, thr, padding)
    for n, run in enumerate(run_timestamps.keys()):

        # tmp variable to collect run's info
        run_attributes = run_timestamps[run]

        phys_in_slices[run] = deepcopy(phys_in[run_attributes[0]:run_attributes[1]])

        # Run check_trigger amount
        phys_in_slices[run].check_trigger_amount(thr=thr,
                                                 num_timepoints_expected=ntp_list[n],
                                                 tr=tr_list[n])

    return phys_in_slices
