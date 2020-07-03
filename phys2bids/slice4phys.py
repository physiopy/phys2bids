#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import logging
from copy import deepcopy

import numpy as np

LGR = logging.getLogger(__name__)


def update_name(basename, **kwargs):
    """
    Add entities, suffix, and/or extension to a BIDS filename while retaining
    BIDS compatibility.

    TODO: Replace list of entities with versioned, yaml entity table from BIDS.
    """
    import os.path as op
    ENTITY_ORDER = ['sub', 'ses', 'task', 'acq', 'ce', 'rec', 'dir', 'run',
                    'mod', 'echo', 'recording', 'proc', 'space', 'split']

    outdir = op.dirname(basename)
    outname = op.basename(basename)

    # Determine scan suffix (should always be physio)
    suffix = outname.split('_')[-1].split('.')[0]
    extension = '.' + '.'.join(outname.split('_')[-1].split('.')[1:])
    filetype = suffix + extension

    for key, val in kwargs.items():
        if key == 'suffix':
            if not val.startswith('_'):
                val = '_' + val

            if not val.endswith('.'):
                val = val + '.'

            outname = outname.replace('_' + suffix + '.', val)
        elif key == 'extension':
            if not val.startswith('.'):
                val = '.' + val
            outname = outname.replace(extension, val)
        else:
            if key not in ENTITY_ORDER:
                raise ValueError('Key {} not understood.'.format(key))

            # entities
            if '_{}-{}'.format(key, val) in basename:
                LGR.warning('Key {} already found in basename {}. '
                            'Skipping.'.format(key, basename))

            elif '_{}-'.format(key) in basename:
                LGR.warning('Key {} already found in basename {}. '
                            'Overwriting.'.format(key, basename))
                regex = '_{}-[0-9a-zA-Z]+'.format(key)
                fname = re.sub(regex, '_{}-{}'.format(key, val), fname)
            else:
                loc = ENTITY_ORDER.index(key)
                entities_to_check = ENTITY_ORDER[loc:]
                entities_to_check = ['_{}-'.format(etc) for etc in entities_to_check]
                entities_to_check.append('_{}'.format(filetype))
                for etc in entities_to_check:
                    if etc in outname:
                        outname = outname.replace(
                            etc,
                            '_{}-{}{}'.format(key, val, etc)
                        )
                        break
    outname = op.join(outdir, outname)
    return outname


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


def slice_phys(phys, run_timestamps):
    """
    Slice a physio object based on run-/file-wise onsets and offsets.
    Adapted from slice4phys with the goal of modularizing slicing functionality
    (i.e., cutting out the run detection step).

    Parameters
    ----------
    phys : BlueprintInput
    run_timestamps : dict
        Each key is a run-wise filename and value is a tuple of (onset, offset),
        where onset and offset are integers corresponding to index values of
        the trigger channel.

    Returns
    -------
    phys_in_slices : dict
        Each key is a run-wise filename (possibly further split by frequency)
        and each value is a BlueprintInput object.
    """
    phys_in_slices = {}
    for i_run, fname in enumerate(run_timestamps.keys()):
        # tmp variable to collect run's info
        run_attributes = run_timestamps[fname]
        trigger_onset, trigger_offset = run_attributes

        unique_frequencies = np.unique(phys.freq)
        trigger_freq = phys.freq[phys.trigger_idx + 1]
        for freq in unique_frequencies:
            # Get onset and offset for the requested frequency
            if freq != trigger_freq:
                onset = int(trigger_onset * trigger_freq / freq)  # no clue if this is right
                offset = int(trigger_offset * trigger_freq / freq)
            else:
                onset = trigger_onset
                offset = trigger_offset

            # Split into frequency-specific object limited to onset-offset
            if len(unique_frequencies) > 1:
                run_fname = update_name(fname, recording=str(freq)+'Hz')
                temp_phys_in = deepcopy(phys[onset:offset])
                not_freq = [i for i in range(len(phys.freq)) if phys.freq[i] != freq]
                temp_phys_in.delete_at_index(not_freq)
                phys_in_slices[run_fname] = temp_phys_in
            else:
                phys_in_slices[fname] = deepcopy(phys[onset:offset])
    return phys_in_slices


def slice4phys(phys_in, ntp_list, tr_list, thr, padding=9):
    """
    Slice runs for phys2bids.

    Parameters
    ---------
    phys_in: BlueprintInput object
        Object returned by BlueprintInput class
    nsec_list: list
        a list of floats given by the user as `nsec` input
        Default: [0, ]
    padding: int, optional
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
