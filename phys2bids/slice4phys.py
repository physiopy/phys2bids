"""Multi-take slicer for phys2bids package."""

import logging
from copy import deepcopy

import numpy as np

LGR = logging.getLogger(__name__)


def find_takes(phys_in, ntp_list, tr_list, thr=None, padding=9):
    """
    Find takes slicing index.

    Returns dictionary key for each take in BlueprintInput object based on
    user's entries. Each key has a tuple of 4 elements, 2 expressing the
    timestamps of take in nb of samples. Timestamps are the index of first and
    last triggers of a take, adjusted with padding. take_start and take_end
    indexes refer to the samples contained in the whole session.
    First trigger time offset and nb of triggers contained in the take are also indicated.

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
    take_timestamps: dictionary
        Containing tuples of take start and end indexes for each take, based on
        trigger channels. It also contains take attributes: time offset from
        session beginning, and nb of triggers in the form of
        take_timestamps{1:(start, end, time offset, nb of triggers),
                       2:(...), ... }
    """
    # Initialize dictionaries to save  take timestamps and phys_in attributes
    take_timestamps = {}

    # Express the padding in samples equivalent
    padding_fr = padding * phys_in.freq[0]

    # enumerate user input  num_timepoints_expected
    for take_idx, take_tps in enumerate(ntp_list):
        # correct time offset for this iteration's object
        phys_in.check_trigger_amount(
            thr=thr, num_timepoints_expected=take_tps, tr=tr_list[take_idx]
        )
        # If it's the very first take, start the take at sample 0,
        # otherwise start is first trigger (adjust with padding later)
        if take_idx == 0:
            take_start = 0
        else:
            take_start = int(np.where(np.isclose(phys_in.timeseries[0], 0))[0])

        # Defining end of acquisition
        # take length in seconds
        end_sec = take_tps * tr_list[take_idx]

        # define index of the take's last trigger + padding (HAS TO BE INT type)
        # pick first value of time array that is over specified take length
        # where returns list of values over end_sec and its dtype, choose [list][first value]
        # Check if end_sec is above the end of the timeseries (it happens for noisy cases)
        if phys_in.timeseries[0][-1] > end_sec:
            take_end = int(np.where(phys_in.timeseries[0] > end_sec)[0][0] + padding_fr)
        else:
            take_end = int(phys_in.timeseries[0].shape[0] - 1)
            LGR.warning(
                f"The computed end point in second was {end_sec}, "
                "but current timeseries only lasts up to "
                f"{phys_in.timeseries[0][-1]}"
            )

        update = int(take_end - padding_fr + 1)

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[0].shape[0] < take_end:
            take_end = phys_in.timeseries[0].shape[0]

        # Adjust timestamps with previous end_index
        # Except if it's the first take
        if take_idx > 0:
            previous_end_index = take_timestamps[take_idx][1]
            # adjust time_offset to keep original timing information
            phys_in.time_offset = phys_in.time_offset + take_timestamps[take_idx][2]
            # update take_start, removing 2 paddings (one for this take, one for the previous)
            take_start = int(take_start + previous_end_index - 2 * padding_fr)
            # update take_end, removing the padding of the previous end
            take_end = int(take_end + previous_end_index - padding_fr)

        # Save *start* and *end_index* in dictionary along with *time_offset* and *ntp found*
        # dict key must be readable by human
        # LGRinfo
        LGR.info(
            "\n--------------------------------------------------------------\n"
            f"Slicing between {(take_start/phys_in.freq[phys_in.trigger_idx])} seconds and "
            f"{take_end/phys_in.freq[phys_in.trigger_idx]} seconds\n"
            "--------------------------------------------------------------"
        )

        take_timestamps[take_idx + 1] = (
            take_start,
            take_end,
            phys_in.time_offset,
            phys_in.num_timepoints_found,
        )

        # update the object so that next iteration will look for the first trigger
        # after previous take's last trigger. maybe padding extends to next take
        phys_in = deepcopy(phys_in[update:-1])

    return take_timestamps


def slice4phys(phys_in, ntp_list, tr_list, thr, padding=9):
    """
    Slice takes for phys2bids.

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
        keys start by `take 1` until last (`take n`).
        items are slices of BlueprintInput objects based on take attributes returned by
        internal function (`slice4phys` takes the same arguments as `find_takes`)
    """
    phys_in_slices = {}
    # inform the user
    LGR.warning(
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        "\nphys2bids will split the input file according to the given -tr and -ntp"
        " arguments"
        "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    )
    # Find the timestamps
    take_timestamps = find_takes(phys_in, ntp_list, tr_list, thr, padding)
    for n, take in enumerate(take_timestamps.keys()):
        # tmp variable to collect take's info
        take_attributes = take_timestamps[take]

        phys_in_slices[take] = deepcopy(phys_in[take_attributes[0] : take_attributes[1]])

        # take check_trigger amount
        phys_in_slices[take].check_trigger_amount(
            thr=thr, num_timepoints_expected=ntp_list[n], tr=tr_list[n]
        )

    return phys_in_slices


def get_onsets_run(trig_MRI, sensitivity=20):
    """
    :param: trig_MRI: numpy array
        MRI trigger time course
    :param: sensitivity: int
        percentile of values to be considered as a 'regular' interval of two consecutive MRI triggers
    :return: onsets_MRI: list
        time points corresponding to when the MRI trigger was received
    :return: run_onset_raw: numpy array
        array of run onsets before visual inspection
    :return: run_offset_raw: numpy array
        array of run offsets before visual inspection
    """

    # convert list to np.array
    onsets_MRI = np.array([int(x) for x in np.where(trig_MRI > np.mean(trig_MRI))[0]])

    # difference of timepoint n and timepoint (n-1)
    difference = (np.array(onsets_MRI[1:]) - np.array(onsets_MRI[0:-1]))
    diff_unique = np.unique(difference)[1:]

    # get threshold of values in which the gap between two time points signify a new run
    check_val = np.percentile(diff_unique, sensitivity)

    # list of gap between two time points to be kept to separate runs
    list_diff_keep = diff_unique[[x > check_val for x in diff_unique]]

    # find position in onsets_MRI where the difference is in list_diff_keep
    run_offset_raw = onsets_MRI[:-1][[d in list_diff_keep for d in difference]]
    run_onset_raw = onsets_MRI[1:][[d in list_diff_keep for d in difference]]

    run_offset_raw = np.append(run_offset_raw, onsets_MRI[-1])
    run_onset_raw = np.insert(run_onset_raw, 0, onsets_MRI[0])

    return onsets_MRI, run_onset_raw, run_offset_raw


def clean_onsets_run_GUI(onsets_MRI, run_onset_raw, run_offset_raw, sampling_rate, padding):
    """
    Visual check of run onsets/ offsets

    :param onsets_MRI: list
        list of indices where the MRI triggers are received
    :param run_onset_raw: numpy array
        array of run onsets
    :param run_offset_raw: numpy array
        array of the run offsets
    :param sampling_rate: int
        sampling frequency of MRI trigger
    :param padding: int
        number of seconds to pad the signal with
    :return: onsets_start: numpy array
        array of run onsets
    :return: onsets_end: numpy array
        array of run offsets
    """

    conditions = np.zeros(max(onsets_MRI) + round(1000 * sampling_rate))
    conditions[onsets_MRI] = 1 # times when MRI triggers are received

    conditions[run_onset_raw] = 1.5
    conditions[run_offset_raw] = -0.5

    data = peakdet.Physio(conditions, fs=sampling_rate)

    data._metadata['peaks'] = run_onset_raw
    data._metadata['troughs'] = run_offset_raw
    data = peakdet.operations.edit_physio(data)

    # return start and end times at (padding) seconds before and after the real on and offsets
    onsets_start = data.peaks - padding*sampling_rate
    onsets_end = data.troughs + padding*sampling_rate

    return onsets_start, onsets_end


def slice_runs(phys_in, onsets, offsets):
    """
    Slice runs according on list of onsets and offsets

    :param phys_in: BlueprintInput
        Object returned by BlueprintInput class
    :param onsets: numpy array
        array of run onsets
    :param offsets: numpy array
        array of run offsets
    :return run_data: dict
        dictionary containing (number of runs) keys and BlueprintInput as values
    """
    run_data = {}

    for i in range(len(offsets)):
        signals = [phys_signal[onsets[i]:offsets[i]] for phys_signal in phys_in.timeseries]
        signals_run = po.BlueprintInput(signals, phys_in.freq, phys_in.ch_name, phys_in.units, phys_in.trigger_idx)

        run_data[i] = signals_run

    return run_data


def split_signal_to_runs(phys_in, manual_check=True, sensitivity=20, padding=9):
    """"
    :param phys_in: BlueprintInput
        Object returned by BlueprintInput class
    :param manual_check: bool
        whether there should be a manual check of the automated on/offsets detection
    :param sensitivity: int
        percentile of values to be considered as a 'regular' interval of two consecutive MRI triggers
    :param padding: int
        number of seconds to pad before and after each run
    :return run_data: dict
        dictionary containing (number of runs) keys and BlueprintInput as values
    """
    trig_MRI = phys_in.timeseries[phys_in.trigger_idx]
    sampling_rate = phys_in.freq[phys_in.trigger_idx]

    # calculate run onsets & offsets
    onsets_MRI, run_onset_raw, run_offset_raw = get_onsets_run(trig_MRI, sensitivity)

    # manual check of run onsets & offsets
    if manual_check:
        onsets_start, onsets_end = clean_onsets_run_GUI(onsets_MRI, run_onset_raw, run_offset_raw, sampling_rate,
                                                        padding)
    else:
        onsets_start = run_onset_raw
        onsets_end = run_offset_raw

    run_signal = slice_runs(phys_in, onsets_start, onsets_end)

    return run_signal, onsets_start, onsets_end

