#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""phys2bids interfaces for loading extension files."""

import logging
import warnings
from copy import deepcopy
from itertools import groupby

import numpy as np

from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)
OPEN_ISSUE = (
    "The file you are trying to convert might not be supported by phys2bids yet. "
    "Please open an issue on GitHub "
    "(https://github.com/physiopy/phys2bids/issues/new/choose) "
    "so that we can improve file support!"
)


def check_multifreq(timeseries, freq, start=0, endat=None):
    """
    Check if there are channels with different frequency than the maximum one.

    Parameters
    ----------
    timeseries : list of numpy.ndarrays
        list of numpy.ndarrays representing channels.
    freq : list of floats
        list with the maximum frequency
    start : int, optional
        first sample of the channel to be considered
    endat : int or None, optional
        last sasmple to consider (None for last)
        Just in case the process takes too long

    Returns
    -------
    multifreq_timeseries : list of numpy.ndarrays
        new list with the channels in their own frequency
    multifreq_freq : list of floats
        new list with the real frequency of the channels
    """
    LGR.info("Checking if frequencies are different across channels")
    multifreq_freq = deepcopy(freq)
    multifreq_timeseries = deepcopy(timeseries)

    # Skip time
    for n, ch in enumerate(timeseries[1:]):
        n = n + 1
        # Find lengths of repetitions
        groups = [list(g) for k, g in groupby(ch[start:endat])]
        count = [len(g) for g in groups]
        # If the file is multifrequency, the greatest common divisor is
        # higher than one and equal to the mode (cause repetitions are possible)
        gcd = np.gcd.reduce(count)
        if gcd > 1 and gcd == max(set(count), key=count.count):
            multifreq_freq[n] = freq[n] / gcd
            multifreq_timeseries[n] = ch[::gcd]

    return multifreq_timeseries, multifreq_freq


def generate_blueprint(timeseries, chtrig, interval, orig_units, orig_names):
    """
    Generate blueprint object from various information.

    Standardize timeseries, chtrig interval orig_units and orig_names in the correct units and
    format and generate a physio_obj.BlueprintInput object.
    This function is mainly thought to adapt txt files.

    Parameters
    ----------
    timeseries : list of numpy.ndarrays
        a list of numpy.ndarrays representing the channels
    chtrig : int
        index of trigger channel, count starts at 1 for human readability
        (and because index 0 is dedicated to time)
    interval : list of strings
        maximum sampling frequency or interval value and unit for the recording.
        Example: ["400", "Hz"]
    orig_units : list of strings
        contains original channels units
    orig_names : list of strings
        contains original channels name

    Returns
    -------
    BlueprintInput

    Raises
    ------
    AttributeError
        If sampling is not in ['min', 'sec', 'µsec', 'msec', 'MHz', 'kHz', 'Hz', 'hr', 'min', 's',
        'ms', 'µs'] reference:
        https://www.adinstruments.com/support/knowledge-base/how-can-channel-titles-ranges-intervals-etc-text-file-be-imported-labchart
        https://www.biopac.com/wp-content/uploads/acqknowledge_software_guide.pdf page 194

    See Also
    --------
    physio_obj.BlueprintInput
    """
    if interval[-1] not in [
        "min",
        "sec",
        "µsec",
        "msec",
        "MHz",
        "kHz",
        "Hz",
        "hr",
        "min",
        "s",
        "ms",
        "µs",
    ]:
        raise AttributeError(
            f'Interval unit "{interval[-1]}" is not in a '
            "valid frequency or time unit format, this probably "
            "means your file is not in min, sec, msec, µsec, hr, min, s, ms, µs, "
            "Mhz, KHz or Hz"
        )
    # Check if the header is in frequency or sampling interval
    if "Hz" in interval[-1]:
        LGR.info(
            "Retrieving frequency from file header, calculating sample interval, "
            "and standardizing to Hz if needed"
        )
        freq = float(interval[0])
        freq_unit = interval[-1]
        if freq_unit == "MHz":
            freq = freq * (1000000)
        elif freq_unit == "kHz":
            freq = freq * 1000
        interval[0] = 1 / freq
        freq = [freq] * len(timeseries)
    else:
        # check if interval is in seconds, if not change the units to seconds and
        # calculate frequency
        if interval[-1] not in ("s", "sec"):
            LGR.warning(
                "Sampling interval not expressed in seconds. " "Converting its value and unit."
            )
            if interval[-1] == "min":
                interval[0] = float(interval[0]) * 60
            elif interval[-1] == "msec":
                interval[0] = float(interval[0]) / 1000
            elif interval[-1] == "µsec":
                interval[0] = float(interval[0]) / 1000000
            elif interval[-1] == "hr":
                interval[0] = float(interval[0]) * 3600
            elif interval[-1] == "ms":
                interval[0] = float(interval[0]) / 1000
            elif interval[-1] == "µs":
                interval[0] = float(interval[0]) / 1000000
            interval[-1] = "s"
        else:
            interval[0] = float(interval[0])
        # get frequency
        freq = [1 / interval[0]] * len(timeseries)
    # reorder channels names
    names = ["time"]
    names = names + orig_names
    # reorder channels units
    units = ["s"]
    units = units + orig_units
    # Check if the file has a time channel, otherwise create it.
    # As the "time" doesn't have a column header, if the number of header names
    # is less than the number of timeseries, then "time" is column 0...
    # ...otherwise, create the time channel
    if not (len(orig_names) < len(timeseries)):
        duration = (timeseries[0].shape[0] + 1) * interval[0]
        t_ch = np.ogrid[0 : duration : interval[0]][:-1]  # create time channel
        timeseries = [
            t_ch,
        ] + timeseries
        freq = [max(freq)] + freq
    timeseries, freq = check_multifreq(timeseries, freq)
    return BlueprintInput(timeseries, freq, names, units, chtrig)


def read_header_and_channels(filename):
    """
    Read a txt file with a header and channels and separate them.

    Parameters
    ----------
    filename : str
        path to the txt Labchart file

    Returns
    -------
    header : list of strings
        header lines
    channel_list : list of strings
        The channels of the recording

    """
    header = []
    # Read in the header until it's numbers
    with open(filename, "r") as f:
        for n, line in enumerate(f):
            line = line.rstrip("\n").split("\t")
            if line[-1] == "":
                line.remove("")
            try:
                float(line[0])
                break
            except ValueError:
                header.append(line)
                continue
    # Read in the rest paying attention to possible differences
    if "Interval=" in header[0]:
        # Not specifying delimiters will ignore comments
        channel_list = np.genfromtxt(filename, skip_header=n)
    elif "acq" in header[0][0]:
        # Specifying delimiters will avoid missing values in the files
        channel_list = np.genfromtxt(filename, skip_header=n, delimiter="\t")
        # Remove extra (empty?) columns, if present
        ch_number = int(header[2][0].split(" ")[0])
        channel_list = channel_list[:, :ch_number]
        # Set all remaining NaNs to 0
        channel_list = np.nan_to_num(channel_list)
        # Take first row and assign it back to header.
        header.append(list(channel_list[0, :].astype(int)))
        channel_list = channel_list[1:, :]

    # Make channel_list a list of singular arrays (one per channel)
    channel_list = [ch for ch in channel_list.T]

    return header, channel_list


def extract_header_items(header):
    """
    Extract interval, orig_units and orig_names from header.

    Extract interval, orig_units and orig_names from header
    depending on the format (AcqKnowledge and labchart)

    Parameters
    ----------
    header : list
        list that contains file header

    Returns
    -------
    interval : list of strings
        maximum sampling frequency or interval value and unit for the recording
    orig_units : list of strings
        contains original channels units
    orig_names : list of strings
        contains original channels name

    Raises
    ------
    NotImplementedError
        If len(header) == 0 and therefore there is no header
        If Labchart headers cannot be processed
        If files are not in acq or txt format
    """
    # check header is not empty and detect if it is in labchart or Acqknoledge format
    if len(header) == 0:
        raise NotImplementedError("Files without header are not supported yet")
    elif "Interval=" in header[0]:
        LGR.info("phys2bids detected that your file is in Labchart format")

        interval = None
        orig_names = None
        range_list = None
        for line in header:
            if "Interval=" in line:
                interval = line[1].split(" ")
            if "ChannelTitle=" in line:
                orig_names = line[1:]
            if "Range=" in line:
                range_list = line[1:]

        if None in [interval, orig_names, range_list]:
            raise NotImplementedError(OPEN_ISSUE)

        orig_units = []
        for item in range_list:
            orig_units.append(item.split(" ")[1])

    elif "acq" in header[0][0]:
        LGR.info("phys2bids detected that your file is in AcqKnowledge format")
        interval = header[1][0].split()
        interval[-1] = interval[-1].split("/")[0]
        # get units and names
        orig_units = []
        orig_names = []
        # the for loop starts at index1 at 3 because that's the first line of the header
        # with channel name info and ends in 2 + twice the number of channels because
        # that should be the last channel name
        for index1 in range(3, 3 + len(header[-1]) * 2, 2):
            orig_names.append(header[index1][0])
            # since units are in the line immediately after we get the units at the same time
            orig_units.append(header[index1 + 1][0])
    else:
        raise NotImplementedError(OPEN_ISSUE)
    return interval, orig_units, orig_names


def load_txt(filename, chtrig=0):
    """
    Read AcqKnowledge and labchart files in .txt format into a BlueprintInput object.

    Parameters
    ----------
    filename : str
        path to the txt Labchart file
    chtrig : int
        index of trigger channel, starting in 1 for human readability

    Returns
    -------
    phys_in
        BlueprintInput object

    See Also
    --------
    physio_obj.BlueprintInput
    """
    header, channel_list = read_header_and_channels(filename)
    interval, orig_units, orig_names = extract_header_items(header)
    phys_in = generate_blueprint(channel_list, chtrig, interval, orig_units, orig_names)
    return phys_in


def load_acq(filename, chtrig=0):
    """
    Populate object phys_input from acq extension files.

    Parameters
    ----------
    filename : str
        path to the txt labchart file
    chtrig : int, optional
        index of trigger channel. Default is 0.

    Returns
    -------
    BlueprintInput

    Note
    ----
    chtrig is not a 0-based Python index - instead, it's human readable (i.e., 1-based).
    This is handy because, when initialising the class, a new channel corresponding
    to time is added at the beginning - that is already taken into account!

    See Also
    --------
    physio_obj.BlueprintInput
    """
    from bioread import read_file

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        data = read_file(filename).channels

    freq = [data[0].samples_per_second]
    timeseries = [data[0].time_index]
    units = ["s"]
    names = ["time"]

    for k, ch in enumerate(data):
        LGR.info(f"{k:02d}. {ch}")
        timeseries.append(ch.data)
        freq.append(ch.samples_per_second)
        units.append(ch.units)
        names.append(ch.name)

    return BlueprintInput(timeseries, freq, names, units, chtrig)


def load_mat(filename, chtrig=0):
    """
    Populate object phys_input from MATLAB files.

    Parameters
    ----------
    filename: str
        path to the txt labchart file
    chtrig : int
        index of trigger channel.
        !!! ATTENTION: IT'S MEANT TO REPRESENT AN INDEX STARTING FROM 1 !!!

    Returns
    -------
    BlueprintInput

    Note
    ----
    chtrig is not a 0-based Python index - instead, it's human readable (i.e., 1-based).
    This is handy because, when initialising the class, a new channel corresponding
    to time is added at the beginning - that is already taken into account!

    See Also
    --------
    physio_obj.BlueprintInput
    """
    # Load MATLAB file into dictionary.
    from pymatreader import read_mat

    mat_dict = read_mat(filename)
    if "__header__" in mat_dict:
        orig_names = list(mat_dict["labels"])
        orig_units = list(mat_dict["units"])
        interval = [mat_dict["isi"], mat_dict["isi_units"]]
        channel_list = mat_dict["data"]
        channel_list = [ch for ch in channel_list.T]
        return generate_blueprint(channel_list, chtrig, interval, orig_units, orig_names)
    else:
        # Convert data into 1d numpy array for easier indexing.
        data = np.squeeze(np.asarray(mat_dict["data"]))

        # Extract number of channels and tick rate.
        n_channels = len(mat_dict["titles"])
        t_freq = mat_dict["tickrate"]

        # Stores MATLAB data into lists.
        timeseries = []
        freq = [
            t_freq,
        ]
        units = [
            "s",
        ]
        names = [
            "time",
        ]

        for ch in range(n_channels):
            units.append(mat_dict["unittext"][int(mat_dict["unittextmap"][ch] - 1)].strip())
            names.append(mat_dict["titles"][ch].strip())
            freq.append(mat_dict["samplerate"][ch])
            idx_start = int(mat_dict["datastart"][ch])
            idx_end = int(mat_dict["dataend"][ch])
            timeseries.append(data[idx_start:idx_end])
        # Calculate duration based on frequency and create time channel.
        interval = 1 / t_freq
        duration = (timeseries[0].shape[0] + 1) * interval
        t_ch = np.ogrid[0:duration:interval][:-1]
        timeseries = [
            t_ch,
        ] + timeseries
        return BlueprintInput(timeseries, freq, names, units, chtrig)


def load_gep(filename):
    """
    Populate object phys_input from GE physiological files.

    Uses the filename that the user provides to find any matching inputs
    from other recording types (PPG, RESP, or ECG).

    **Note that the filename must not be altered from how it is output from
    the scanner.**

    Populates physio_obj with all identified recording types (note that one
    or more of these may not be true recordings as the scanner outputs all
    possible types in all cases). The modality corresponding to the filename
    entered by the user is put first (after time and trigger).

    Parameters
    ----------
    filename: str
        path to the GE scanner physiological file

    Returns
    -------
    BlueprintInput

    Note
    ----

    GE physiological files do not record a trigger so a column is added at
    position 1. This has a value of zero up to the scan start time and then
    a value of one for the duration of the scan.

    See Also
    --------
    physio_obj.BlueprintInput
    """
    import os
    from glob import glob
    from pathlib import Path

    # Initiate lists of column names and units with time and trigger
    names = ["time", "trigger"]
    units = ["s", "mV"]  # Assuming recording units are mV...

    # Add column for file given by user
    if "PPGData" in filename:
        freq = [100, 100, 100]
        names.append("cardiac")
    elif "RESPData" in filename:
        freq = [25, 25, 25]
        names.append("respiratory")
    elif "ECGData" in filename:
        freq = [1000, 1000, 1000]
        names.append("cardiac")

    # Load in user file data
    data = [np.loadtxt(filename)]

    # Calculate time in seconds for first input (starts from -30s)
    interval = 1 / freq[0]
    duration = data[0].shape[0] * interval
    t_ch = np.ogrid[-30 : duration - 30 : interval]

    # Find and add additional data files
    filename = Path(filename)
    fnames = glob(os.path.join(filename.parent, f"*{filename.name[-24:-4]}.gep"))
    fnames.remove(str(filename))  # Drop the original file
    if not len(fnames) == 0:
        for fname in fnames:
            if "PPGData" in fname:
                freq.append(100)
                names.append("cardiac")
                data.append(np.loadtxt(fname))
            elif "RESPData" in fname:
                freq.append(25)
                names.append("respiratory")
                data.append(np.loadtxt(fname))
            elif "ECGData" in fname:
                freq.append(1000)
                names.append("cardiac")
                data.append(np.loadtxt(fname))

    # Create trigger channel
    trigger = np.hstack((np.zeros(int(30 / interval)), np.ones(int((duration - 30) / interval))))

    # Create final list of timeseries
    timeseries = [t_ch, trigger]
    timeseries.extend(data)
    return BlueprintInput(timeseries, freq, names, units, 1)


def load_smr(filename, chtrig=0):
    """Load Spike2 smr file and populate object phys_input.

    Parameters
    ----------
    filename: str
        Path to the spike smr or smrx file.

    chtrig : int
        Index of trigger channel.

    Returns
    -------
    BlueprintInput

    Note
    ----
    Index of chtrig is 1-index (i.e. spike2 channel number).

    See Also
    --------
    physio_obj.BlueprintInput
    """
    import sonpy

    # taken from sonpy demo
    read_data = {
        sonpy.lib.DataType.Adc: sonpy.lib.SonFile.ReadInts,
        sonpy.lib.DataType.EventFall: sonpy.lib.SonFile.ReadEvents,
        sonpy.lib.DataType.EventRise: sonpy.lib.SonFile.ReadEvents,
        sonpy.lib.DataType.EventBoth: sonpy.lib.SonFile.ReadEvents,
        sonpy.lib.DataType.Marker: sonpy.lib.SonFile.ReadMarkers,
        sonpy.lib.DataType.AdcMark: sonpy.lib.SonFile.ReadWaveMarks,
        sonpy.lib.DataType.RealMark: sonpy.lib.SonFile.ReadRealMarks,
        sonpy.lib.DataType.TextMark: sonpy.lib.SonFile.ReadTextMarks,
        sonpy.lib.DataType.RealWave: sonpy.lib.SonFile.ReadFloats,
    }

    smrfile = sonpy.lib.SonFile(filename, True)
    time_base = smrfile.GetTimeBase()
    n_channels = smrfile.MaxChannels()
    freq, names, units, timeseries = [], [], [], []
    for i in range(n_channels):
        current_channel = smrfile.ChannelType(i)
        max_n_tick = smrfile.ChannelMaxTime(i)
        if current_channel != sonpy.lib.DataType.Off and max_n_tick > 0:
            max_n_tick = smrfile.ChannelMaxTime(i)
            sample_rate = smrfile.GetIdealRate(i)
            if current_channel == sonpy.lib.DataType.Adc:
                divide = smrfile.ChannelDivide(i)
            else:  # marker channels
                divide = 1 / (time_base * sample_rate)
            # conversion factor from CED spike2 doc
            # http://ced.co.uk/img/Spike9.pdf
            gain = smrfile.GetChannelScale(i) / 6553.6
            offset = smrfile.GetChannelOffset(i)
            name = smrfile.GetChannelTitle(chan=i)
            unit = smrfile.GetChannelUnits(chan=i)

            n_samples = int(np.floor((max_n_tick) / divide))
            raw_signal = read_data[current_channel](
                smrfile, chan=i, nMax=n_samples, tFrom=0, tUpto=max_n_tick
            )

            signal = np.array(raw_signal) * gain + offset

            # save the data
            freq.append(sample_rate)
            names.append(name)
            units.append(unit)
            timeseries.append(signal)

    # use the channel with highest sample rate to create time stamps
    idx_max = np.argmax(freq)
    n_timepoints = len(timeseries[idx_max])  # end point included
    time = np.arange(n_timepoints) * freq[idx_max]

    # prepend to the existing list
    freq = [freq[idx_max]] + freq
    timeseries = [time] + timeseries
    units = ["s"] + units
    names = ["time"] + names
    return BlueprintInput(timeseries, freq, names, units, chtrig)
