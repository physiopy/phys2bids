"""Multi-take slicer for phys2bids package."""

import logging
from copy import deepcopy

import numpy as np

LGR = logging.getLogger(__name__)


def estimate_ntp_and_tr(phys_in, thr=None, ci=1):
    """
    Find groups of trigger in a spiky signal like the trigger channel signal.

    Parameters
    ----------
    phys_in : BlueprintInput object
        A BlueprintInput object containing a physiological acquisition
    thr : None, optional
        The threshold for automatic spike detection. Default is to use the average of
        the signal.
    ci : int or float, optional
        Confidence Interval (CI) to use in the estimation of the trigger clusters. The
        cluster algorithm considers triggers with duration (in samples) within this CI
        as part of the same group, thus the same. If CI is an integer, it will consider
        that amount of samples. If CI is a float and < 1, it will consider that
        percentage of the trigger duration. CI cannot be a float > 1. Default is 1.
        Change to .25 if there is a CMRR DWI sequence or when recording sub-triggers.

    Returns
    -------
    ntp
        The list of number of timepoints found for each take.
    tr
        The list of corresponding TR, computed as average samples per group / frequency.

    Raises
    ------
    Exception
        If it doesn't find at least one group.
    ValueError
        If CI is a float above 1 or if it is not an int or a float.
    """
    LGR.info('Running automatic clustering of triggers to find timepoints and tr of each "take"')
    trigger = phys_in.timeseries[phys_in.trigger_idx]

    thr = np.mean(trigger) if thr is None else thr
    timepoints = trigger > thr
    spikes = np.flatnonzero(np.ediff1d(timepoints.astype(np.int8)) > 0)
    interspike_interval = np.diff(spikes)
    unique_isi, counts = np.unique(interspike_interval, return_counts=True)

    # The following line is for python < 3.12. From 3.12, ci.is_integer() is enough.
    if isinstance(ci, int) or isinstance(ci, float) and ci.is_integer():
        upper_ci_isi = unique_isi + ci
    elif isinstance(ci, float) and ci < 1:
        upper_ci_isi = unique_isi * (1 + ci)
    elif isinstance(ci, float) and ci > 1:
        raise ValueError("Confidence intervals percentages above 1 are not supported.")
    else:
        raise ValueError("Confidence intervals must be either integers or floats.")

    # Loop through the uniques ISI and group them within the specified CI.
    # Also compute the average TR of the group.
    isi_groups = {}
    average_tr = {}
    k = 0
    current_group = [unique_isi[0]]

    # np.unique returns sorted elements → unique_isi[0] == min(unique_isi), so THIS WORKS.
    for n, i in enumerate(range(1, len(unique_isi))):
        if unique_isi[i] <= upper_ci_isi[n]:
            current_group.append(unique_isi[i])
        else:
            isi_groups[k] = current_group
            average_tr[k] = np.mean(current_group) / phys_in.freq[0]
            k += 1
            current_group = [unique_isi[i]]

    isi_groups[k] = current_group
    average_tr[k] = np.mean(current_group) / phys_in.freq[0]

    # Invert the isi_group into value per group
    group_by_isi = {isi: group for group, isis in isi_groups.items() for isi in isis}

    # Use the found groups to find the number of timepoints and assign the right TR
    estimated_ntp = []
    estimated_tr = []

    i = 0
    while i < interspike_interval.size - 1:
        current_group = group_by_isi.get(interspike_interval[i])
        for n in range(i + 1, interspike_interval.size):
            if current_group != group_by_isi.get(interspike_interval[n]):
                break
        # Repeat one last time outside of for loop
        estimated_ntp += [n - i]
        estimated_tr += [average_tr[current_group]]
        i = n

    if len(estimated_ntp) < 1:
        raise Exception("This should not happen. Something went very wrong.")
    # The algorithm found n groups, the last of which has two timepoints less due to
    # diff computations. Each real group of n>1 triggers counts one trigger less but is
    # followed by a "fake" group of 1 trigger that is actually the interval to the next
    # group. That does not hold if there is a real group of 1 trigger.
    # Loop through the estiamtions to fix all that.
    ntp = []
    tr = []
    i = 0

    while i < len(estimated_ntp):
        if estimated_ntp[i] == 1:
            ntp.append(estimated_ntp[i])
            tr.append(estimated_tr[i])
            i += 1
        elif i + 1 < len(estimated_ntp):
            ntp.append(estimated_ntp[i] + estimated_ntp[i + 1])
            tr.append(estimated_tr[i])
            i += 2
        else:
            ntp.append(estimated_ntp[i] + 2)
            tr.append(estimated_tr[i])
            i += 1

    LGR.info(
        f"The automatic clustering found {len(ntp)} groups of triggers long: {ntp} with respective TR: {tr}"
    )
    return ntp, tr


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
            take_start = int(np.argmax(np.isclose(phys_in.timeseries[0], 0)))

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
