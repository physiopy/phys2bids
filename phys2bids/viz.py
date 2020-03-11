# -*- coding: utf-8 -*-
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
    Produces a textfile of the specified extension `ext`,
    containing the given content `text`.

    Parameters
    ----------
    time: numpy ndarray
        time channel
    trigger: numpy ndarray
        trigger channel
    fileprefix: str or path
        A string representing a file name or a fullpath
        to a file, WITHOUT extension
    filename: string
        name of the original file
    options: argparse object
        The object produced by `get_parser` in `cli.run.py`
    figsize: tuple
        Desired size of the figure (see `matplotlib`),
        Default is {FIGSIZE}
    dpi: int
        Desired DPI of the figure (see `matplotlib`),
        Default is {SET_DPI}

    Notes
    -----
    Outcome:
    fileprefix + _trigger_time.png:
        Creates new plot `fileprefix_trigger_time.png`.
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
    subplot = fig.add_subplot(311)
    subplot.set_title(f'Trigger and time for {outname}.tsv.gz')
    subplot.set_ylim([-0.2, thr * 3])
    subplot.set_xlabel('Seconds')
    subplot.set_ylabel('Volts')
    subplot.plot(time, trigger, '-', time, thrline, 'r-.', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    # plot the first spike according to the user threshold
    subplot = fig.add_subplot(323)
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
    ax2.set_title('Initial trigger for selected threshold')
    # plot the last spike according to the user threshold
    subplot = fig.add_subplot(324)
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
    ax2.set_title('Last trigger for selected threshold')
    subplot.plot(time, trigger, '-', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    # lets do the suggested threshold plot
    trigger_idx = (range(len(trigger)))
    thr_idex = [i for (i, j) in zip(trigger_idx, trigger) if j >= thr]
    new_thr = thr
    # if the threshold doesn't get any trigger points
    while thr_idex == []:
        new_thr = new_thr / 1.5
        thr_idex = [i for (i, j) in zip(trigger_idx, trigger) if j >= new_thr]
    new_thr = np.round(new_thr, decimals=2)
    # plot the first spike according to the suggested threshold
    subplot = fig.add_subplot(325)
    subplot.set_xlim([time[thr_idex[-0]] - 4, time[thr_idex[-0]] + 4])
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
    # tr_array = []
    # for sample in time:
    #     tr_array.append(time2ntr(sample))
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    ax2.set_xlabel('TR')
    subplot.plot(time, trigger, '-', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    ax2.set_title(f'Initial trigger for suggested threshold {new_thr}')
    # plot the last spike according to the suggested threshold
    subplot = fig.add_subplot(326)
    subplot.set_xlim([time[thr_idex[-1]] - 4,
                      time[thr_idex[-1]] + 4])
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
    # tr_array = []
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    ax2.set_xlabel('TR')
    ax2.set_title(f'Last trigger for suggested threshold {new_thr}')
    subplot.plot(time, trigger, '-', time, block, '-')
    subplot.fill_between(time, block, where=block >= d, interpolate=True, color='#ffbb6e')
    plt.savefig(fileprefix + '_trigger_time.png', dpi=dpi)
    plt.close()


def plot_all(phys_in, infile, outfile='', dpi=SET_DPI, size=FIGSIZE):
    ch_num = len(phys_in.ch_name)  # get number of channels:
    fig, ax = plt.subplots(ch_num - 1, 1, figsize=size, sharex=True)
    time = phys_in.timeseries[0]  # assume time is first channel
    fig.suptitle(os.path.basename(infile))
    for row, timeser in enumerate(phys_in.timeseries[1:]):
        if timeser.shape != time.shape:
            time_old = np.linspace(0, time[-1], num=timeser.shape[0])
            timeser = np.interp(time, time_old, timeser)
        ax[row].plot(time, timeser)
        ax[row].set_title(f' Channel {row + 1}: {phys_in.ch_name[row + 1]}')
        ax[row].set_ylabel(phys_in.units[row + 1])
        ax[row].xlim = 30 * 60 * phys_in.freq[0]  # maximum display of half an hour
        ax[row].grid()
    ax[row].set_xlabel("seconds")
    if outfile == '':
        outfile = os.path.splitext(os.path.basename(infile))[0] + '.png'
    LGR.info(f'saving channel plot to {outfile}')
    fig.savefig(outfile, dpi=dpi, bbox_inches='tight')
