# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

SET_DPI = 100
FIGSIZE = (18, 10)


def plot_channel(table, channel, filename, figsize=FIGSIZE, dpi=SET_DPI):
    plt.figure(figsize=figsize, dpi=dpi)
    plt.title(channel)
    plt.plot(table.index.values, table[channel], '-')
    plt.savefig(filename + '_' + channel + '_time.png', dpi=dpi)
    plt.close()


def plot_trigger(time, trigger, outfile, options, figsize=FIGSIZE, dpi=SET_DPI):
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
    plt.savefig(outfile + '_trigger_time.png', dpi=dpi)
    plt.close()

def plot_all(phys_in,infile,outfile,dpi = SET_DPI,size = FIGSIZE):
    ch_num = len(phys_in.ch_name) # get number of channels:
    fig,ax = plt.subplots(ch_num-1,1,figsize = size,sharex=True)
    row = 0
    time = phys_in.timeseries[0] # assume time is first channel
    fig.suptitle(infile)
    for index, timeser in enumerate(phys_in.timeseries[1:]):
        index += 1
        ax[row].plot(time,timeser)
        ax[row].set_title(f' Channel {index + 1}: {phys_in.ch_name[index]}')
        ax[row].set_ylabel(phys_in.units[index-1])
        ax[row].xlim=30*60*phys_in.freq[0] # maximum display of half an hour
        ax[row].grid()
        row += 1
    ax[row-1].set_xlabel("seconds")
    fig.savefig(outfile,dpi = dpi,bbox_inches = 'tight')

