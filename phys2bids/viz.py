# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from .physiobids import FIGSIZE, SET_DPI


def print_plot(table, channel, filename):
    plt.figure(figsize=FIGSIZE, dpi=SET_DPI)
    plt.title(channel)
    plt.plot(table.index.values, table[channel], '-')
    plt.savefig(filename + '_' + channel + '_time.png', dpi=SET_DPI)
    plt.close()


def plot_trigger(time, trigger, outfile, options):
    def time2ntr(x):
        return x / options.tr

    def ntr2time(x):
        return x * options.tr

    thrline = np.ones(time.shape) * options.thr
    fig = plt.figure(figsize=FIGSIZE, dpi=SET_DPI)
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
    subplot.set_xlim([options.tr * (options.num_tps_expected - 4),
                      options.tr * (options.num_tps_expected + 4)])
    subplot.set_ylim([-0.2, options.thr * 3])
    subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
    subplot.plot(time, trigger, '-', time, time, '-')
    plt.savefig(outfile + '_trigger_time.png', dpi=SET_DPI)
    plt.close()
