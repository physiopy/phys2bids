"""Visualization functions for phys2bids package."""
import os
import logging

import matplotlib.pyplot as plt
import numpy as np

LGR = logging.getLogger(__name__)

SET_DPI = 100
FIGSIZE = (18, 10)


def plot_trigger(time, trigger, fileprefix, tr, thr, num_timepoints_expected,
                 filename, figsize=FIGSIZE, dpi=SET_DPI):
    """
    Produce a figure with three plots.

    1. Plots the triggers in blue, a block in orange that indicates
    the time from the first trigger to the last, and a red line showing
    the threshold used for trigger detection
    2. Same plot but showing only the intial trigger
    3. Same plot but showing only the intial trigger

    Parameters
    ----------
    time: numpy ndarray
        time channel
    trigger: numpy ndarray
        trigger channel
    fileprefix: str or path
        A string representing a file name or a fullpath
        to a file, WITHOUT extension
    tr: float
        Repetition time
    thr: float
        Threshold used to detect the number of triggers
    num_timepoints_expected: int
        Number of timepoints expected by the user
    filename: string
        name of the original file
    figsize: tuple or list of floats
        Size of the figure expressed as (size_x, size_y),
        Default is {FIGSIZE}
    dpi: int
        Desired DPI of the figure,
        Default is {SET_DPI}

    Notes
    -----
    Outcome:
    fileprefix + _trigger_time.png:
        Creates new plot `fileprefix_trigger_time.png`.

    See Also
    --------
    https://phys2bids.readthedocs.io/en/latest/howto.html
    matplotlib.pyploy.figsize
    """

    def time2ntr(x):
        return x / tr

    def ntr2time(x):
        return x * tr
    # get filename
    outname = os.path.splitext(os.path.basename(filename))[0]
    # create threshold line
    thrline = np.ones(time.shape) * thr
    # define figure and space between plots
    fig = plt.figure(figsize=figsize, dpi=dpi)
    block = time > 0
    d = np.zeros(len(time))
    plt.subplots_adjust(hspace=0.7)
    # plot of the hole trigger
    subplot = fig.add_subplot(211)
    subplot.set_title(f'Trigger and time for {outname}.tsv.gz')
    subplot.set_ylim([-0.2, thr * 3])
    subplot.set_xlabel('Seconds')
    subplot.set_ylabel('Volts')
    subplot.plot(time, trigger, '-', time, thrline, 'r-.', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    subplot.legend(['trigger', 'Trigger detection threshold', 'time block'], loc='upper right')
    # plot the first spike according to the user threshold
    subplot = fig.add_subplot(223)
    subplot.set_xlim([-tr * 4, tr * 4])
    subplot.set_ylim([-0.2, thr * 3])
    subplot.set_xlabel('Seconds')
    subplot.set_ylabel('Volts')
    ax2 = subplot.twiny()
    ax2.set_xticklabels('')
    ax2.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False,
                    pad=15)
    # add secondary axis ticks
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    # add secondary axis labelS
    ax2.set_xlabel('TR')
    subplot.plot(time, trigger, '-', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    ax2.set_title('Starting triggers for selected threshold')
    # plot the last spike according to the user threshold
    subplot = fig.add_subplot(224)
    subplot.set_xlim([tr * (num_timepoints_expected) - 4,
                      tr * (num_timepoints_expected) + 4])
    subplot.set_xlabel('Seconds')
    subplot.set_ylabel('Volts')
    subplot.set_ylim([-0.2, thr * 3])
    ax2 = subplot.twiny()
    ax2.set_xticklabels('')
    ax2.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False,
                    pad=15)
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    ax2.set_xlabel('TR')
    ax2.set_title('Ending triggers for selected threshold')
    subplot.plot(time, trigger, '-', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    if 'PYTEST_CURRENT_TEST' not in os.environ:
        plt.savefig(fileprefix + '_trigger_time.png', dpi=dpi)
    plt.close()


def export_trigger_plot(phys_in, chtrig, fileprefix, tr, num_timepoints_expected,
                        filename, sub=None, ses=None, figsize=FIGSIZE,
                        dpi=SET_DPI):
    """
    Save a trigger plot.

    Used in main workflow (`phys2bids`), this function minimizes repetition in code for parallel
    workflow (multi-run workflow and default workflow) and maintains readability of code

    Parameters
    ---------
    phys_in : object
        Object returned by BlueprintInput class
        For multi-run acquisitions, phys_in is a slice of the whole object
    chtrig : int
        trigger channel
        integer representing the index of the trigger on phys_in.timeseries
    fileprefix: str or path
        A string representing a file name or a fullpath
        to a file, WITHOUT extension
    tr : list
        a list of float given by the user as `tr` input
    num_timepoints_expected : list
        a list of integers given by the user as `ntp` input
    filename : str
        name of the input file given by user's entry
    sub: str or int
        Name of subject. Default is None
    ses: str or int or None
        Name of session. Default is None
    figsize: tuple or list of floats
        Size of the figure expressed as (size_x, size_y),
        Default is {FIGSIZE}
    dpi: int
        Desired DPI of the figure,
        Default is {SET_DPI}
    """
    LGR.info('Plot trigger')
    # Create trigger plot. If possible, to have multiple outputs in the same
    # place, adds sub and ses label.
    if sub is not None:
        fileprefix += f'_sub-{sub}'
    if ses is not None:
        fileprefix += f'_ses-{ses}'

    # adjust for multi run arguments, iterate through acquisition attributes
    plot_trigger(phys_in.timeseries[0], phys_in.timeseries[chtrig],
                 fileprefix, tr, phys_in.thr, num_timepoints_expected,
                 filename, figsize, dpi)


def plot_all(ch_name, timeseries, units, freq, infile, outfile, dpi=SET_DPI, size=FIGSIZE):
    """
    Plot all the channels for visualizations and saves them in outfile.

    Parameters
    ----------
    ch_name: (ch) list of strings
        List of names of the channels - can be the header of the columns
        in the output files.
    timeseries: (ch, [tps]) list
        List of numpy 1d arrays - one for channel, plus one for time.
        Time channel has to be the first, trigger the second.
        Contains all the timeseries recorded.
    units: (ch) list of strings
        List of the units of the channels.
    freq: (ch) list of floats
        List of floats - one per channel.
        Contains all the frequencies of the recorded channel.
    infile: string
        name of the input file to phys2bids
    outfile: string
        path of the output plot
    dpi: int
        Desired DPI of the figure,
        Default is {SET_DPI}
    figsize: tuple or list of floats
        Size of the figure expressed as (size_x, size_y),
        Default is {FIGSIZE}
    -----
    outcome:
        Creates new plot with path specified in outfile.

    See Also
    --------
    https://phys2bids.readthedocs.io/en/latest/howto.html
    matplotlib.pyploy.figsize
    """
    ch_num = len(ch_name)  # get number of channels:
    fig, ax = plt.subplots(ch_num - 1, 1, figsize=size, sharex=True)
    time = timeseries[0]  # assume time is first channel
    fig.suptitle(os.path.basename(infile))
    for row, timeser in enumerate(timeseries[1:]):
        if timeser.shape != time.shape:
            time_old = np.linspace(0, time[-1], num=timeser.shape[0])
            timeser = np.interp(time, time_old, timeser)
        ax[row].plot(time, timeser)
        ax[row].set_title(f' Channel {row + 1}: {ch_name[row + 1]}')
        ax[row].set_ylabel(units[row + 1])
        ax[row].xlim = 30 * 60 * freq[0]  # maximum display of half an hour
        ax[row].grid()
    ax[row].set_xlabel('seconds')
    outfile = os.path.join(outfile, os.path.splitext(os.path.basename(infile))[0] + '.png')
    LGR.info(f'saving channel plot to {outfile}')
    fig.savefig(outfile, dpi=dpi, bbox_inches='tight')
