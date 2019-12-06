# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

SET_DPI = 100
FIGSIZE = (18, 10)


def plot_channel(table, channel, fileprefix, figsize=FIGSIZE, dpi=SET_DPI):
    """
    Produces a textfile of the specified extension `ext`,
    containing the given content `text`.

    Input
    -----
    table: pandas dataframe
        Dataframe containing channels
    channel: str
        name of the desired channel (`table` column)
    fileprefix: str or path
        A string representing a file name or a fullpath
        to a file, WITHOUT extension
    figsize: tuple
        Desired size of the figure (see `matplotlib`),
        Default is {FIGSIZE}
    dpi: int
        Desired DPI of the figure (see `matplotlib`),
        Default is {SET_DPI}

    Outcome
    -------
    fileprefix + '_' + channel + '_time.png':
        Creates new plot `fileprefix_channel_time.png`.
    """

    plt.figure(figsize=figsize, dpi=dpi)
    plt.title(channel)
    plt.plot(table.index.values, table[channel], '-')
    plt.savefig(fileprefix + '_' + channel + '_time.png', dpi=dpi)
    plt.close()


def plot_trigger(time, trigger, fileprefix, options, figsize=FIGSIZE, dpi=SET_DPI):
    """
    Produces a textfile of the specified extension `ext`,
    containing the given content `text`.

    Input
    -----
    time: numpy ndarray
        time channel
    trigger: numpy ndarray
        trigger channel
    fileprefix: str or path
        A string representing a file name or a fullpath
        to a file, WITHOUT extension
    options: argparse object
        The object produced by `get_parser` in `cli.run.py`
    figsize: tuple
        Desired size of the figure (see `matplotlib`),
        Default is {FIGSIZE}
    dpi: int
        Desired DPI of the figure (see `matplotlib`),
        Default is {SET_DPI}

    Outcome
    -------
    fileprefix + _trigger_time.png:
        Creates new plot `fileprefix_trigger_time.png`.
    """

    def time2ntr(x):
        return x / options.tr

    def ntr2time(x):
        return x * options.tr

    thrline = np.ones(time.shape) * options.thr
    fig = plt.figure(figsize=figsize, dpi=dpi)
    subplot = fig.add_subplot(211)
    subplot.set_title('trigger and time')
    subplot.set_ylim([-0.2, options.thr * 10])
    subplot.plot(time, trigger, '-', time, thrline, 'r-.', time, time, '-')
    subplot = fig.add_subplot(223)
    subplot.set_xlim([-options.tr * 4, options.tr * 4])
    subplot.set_ylim([-0.2, options.thr * 3])
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    subplot.plot(time, trigger, '-', time, time, '-')
    subplot = fig.add_subplot(224)
    subplot.set_xlim([options.tr * (options.num_timepoints_expected - 4),
                      options.tr * (options.num_timepoints_expected + 4)])
    subplot.set_ylim([-0.2, options.thr * 3])
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    subplot.plot(time, trigger, '-', time, time, '-')
    plt.savefig(fileprefix + '_trigger_time.png', dpi=dpi)
    plt.close()
