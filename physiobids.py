#!/usr/bin/env python3

"""
Phys2bids is a python3 library meant to set physiological files in BIDS
standard.
It was born for Acqknowledge files (BIOPAC), and at the moment it supports
``.acq`` files and ``.txt`` files obtained by labchart
(ADInstruments) and Respiract.

It requires python 3.6 or above, as well as the modules:
- `numpy`
- `pandas`
- `matplotlib`

In order to process ``.acq`` files, it needs `bioread`, an excellent module
that can be found at `this link`_

The project is under development.

At the very moment, it assumes all the extracted channels from a file
have the same sampling freq.

.. _this link:
   https://github.com/uwmadison-chm/bioread
"""

import os
import argparse
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


VERSION = '0.3.0'
SET_DPI = 100
FIGSIZE = (18, 10)
# #!# This is hardcoded until we find a better solution
HEADERLENGTH = 9


# #!# Different frequencies == different files!


def _version_():
    print('physiobids v.' + VERSION)


def _get_parser():
    """
    Parses command line inputs for this function

    Returns
    -------
    parser.parse_args() : argparse dict

    """
    parser = argparse.ArgumentParser()
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required Argument:')
    required.add_argument('-in', '--input-file',
                          dest='filename',
                          type=str,
                          help=('The name of the acq file, with or without '
                                'extension.   Must be an .acq file!'),
                          required=True)
    optional.add_argument('-info', '--info',
                          dest='info',
                          action='store_true',
                          help='Only output file info, don\'t process.',
                          default=False)
    optional.add_argument('-indir', '--input-dir',
                          dest='indir',
                          type=str,
                          help='Folder containing input.',
                          default='.')
    optional.add_argument('-outdir', '--output-dir',
                          dest='outdir',
                          type=str,
                          help=('Folder where output should be placed.'
                                'If \"-heur\" is used, it\'ll become '
                                'the site folder. Requires \"-sub\",'
                                ' and it\'s possible to specify \"-ses\""'),
                          default='.')
    optional.add_argument('-heur', '--heuristic',
                          dest='heur_file',
                          type=str,
                          help=('File containing heuristic, with or without '
                                'extension. Specify path to it if necessary.'),
                          default=None)
    # optional.add_argument('-hdir', '--heur-dir',
    #                       dest='heurdir',
    #                       type=str,
    #                       help='Folder containing heuristic file.',
    #                       default='.')
    optional.add_argument('-sub', '--subject',
                          dest='sub',
                          type=str,
                          help=('To be specified with \"-heur\". Code of '
                                'subject to process.'
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-ses', '--session',
                          dest='ses',
                          type=str,
                          help=('To be specified with \"-heur\". Code of '
                                'session to process.'
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-chtrig', '--channel-trigger',
                          dest='chtrig',
                          type=int,
                          help=('The number corresponding to the trigger channel.'
                                ' Channel numbering starts with 0'),
                          default=1)
    optional.add_argument('-chsel', '--channel-selection',
                          dest='chsel',
                          nargs='*',
                          type=int,
                          help='The number corresponding to the channels to process.',
                          default=None)
    optional.add_argument('-ntp', '--numtps',
                          dest='num_tps_expected',
                          type=int,
                          help='Number of expected timepoints.',
                          default=340)  # #!# Has to go to 0
    optional.add_argument('-tr', '--tr',
                          dest='tr',
                          type=float,
                          help='TR of sequence in seconds.',
                          default=1.5)  # #!# Has to go to 0
    optional.add_argument('-thr', '--threshold',
                          dest='thr',
                          type=float,
                          help='Threshold used for trigger detection.',
                          default=2.5)
    optional.add_argument('-tbhd', '--table-header',
                          dest='table_header',
                          nargs='*',
                          type=str,
                          help='Columns header (for json file).',
                          default=['time', 'respiratory_chest', 'trigger',
                                   'cardiac', 'respiratory_CO2', 'respiratory_O2'])  # #!# Has to go to empty list
    optional.add_argument('-v', '--version', action='version', version=('%(prog)s ' + VERSION))

    parser._action_groups.append(optional)

    return parser


def check_input_dir(indir):
    if indir[-1:] == '/':
        indir = indir[-1:]

    return indir


def check_input_ext(file, ext):
    if file[-len(ext):] != ext:
        file = file + ext

    return file


def path_exists_or_make_it(fldr):
    """
    Check if folder exists, if not make it
    """
    if not os.path.isdir(fldr):
        os.makedirs(fldr)


def check_file_exists(file, hardexit=True):
    """
    Check if file exists.
    """
    if not os.path.isfile(file) and file is not None:
        print('The file ' + file + ' does not exist!')
        sys.exit()


def move_file(oldpath, newpath, ext=''):
    """
    Moves file from oldpath to newpath.
    If file already exists, remove it first.
    """
    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    os.rename(oldpath + ext, newpath + ext)


def copy_file(oldpath, newpath, ext=''):
    """
    Copy file from oldpath to newpath.
    If file already exists, remove it first.
    """
    from shutil import copy as cp

    check_file_exists(oldpath + ext)

    if os.path.isfile(newpath + ext):
        os.remove(newpath + ext)

    cp(oldpath + ext, newpath + ext)


def print_plot(table, channel, filename):
    plt.figure(figsize=FIGSIZE, dpi=SET_DPI)
    plt.title(channel)
    plt.plot(table.index.values, table[channel], '-')
    plt.savefig(filename + '_' + channel + '_time.png', dpi=SET_DPI)
    plt.close()


def writefile(filename, ext, text):
    with open(filename + ext, 'w') as text_file:
        print(text, file=text_file)


def print_info_acq(filename, data):
    print('File ' + filename + ' contains:\n')
    for ch in range(0, len(data)):
        print(str(ch) + ': ' + data[ch].name)


def print_info_txt(filename):
    with open(filename) as txtfile:
        header = [next(txtfile) for x in range(HEADERLENGTH-2)]

    del header[1:4]
    del header[2]

    print('File ' + filename + ' contains:\n')
    for line in header:
        print(line)

    return header


def print_summary(filename, ntp_expected, ntp_found, samp_freq, time_offset, outfile):
    start_time = -time_offset
    summary = (f'------------------------------------------------\n'
               f'Filename:            {filename}\n'
               f'\n'
               f'Timepoints expected: {ntp_expected}\n'
               f'Timepoints found:    {ntp_found}\n'
               f'Sampling Frequency:  {samp_freq} Hz\n'
               f'Sampling started at: {start_time} s\n'
               f'Tip: Time 0 is the time of first trigger\n'
               f'------------------------------------------------\n')
    print(summary)
    writefile(outfile, '.log', summary)


def print_json(filename, samp_freq, time_offset, table_header):
    start_time = -time_offset
    summary = (f'{{\n'
               f'\t\"SamplingFrequency\": \"{samp_freq} Hz\",\n'
               f'\t\"StartTime\": {start_time},\n'
               f'\t\"Columns\": \"{table_header}\"\n'
               f'}}')  # check table header
    writefile(filename, '.json', summary)


def use_heuristic(heur_file, sub, ses, filename, outdir):
    check_file_exists(heur_file)

    from importlib import import_module

    if sub[:4] != 'sub-':
        name = 'sub-' + sub
    else:
        name = sub

    fldr = outdir + '/' + name

    if ses:
        if ses[:4] != 'ses-':
            fldr = fldr + '/ses-' + ses
            name = name + '_ses-' + ses
        else:
            fldr = fldr + '/' + ses
            name = name + ses

    fldr = fldr + '/func'
    path_exists_or_make_it(fldr)

    cwd = os.getcwd()
    os.chdir(outdir)
    copy_file(heur_file,'./heur.py')

    heur = import_module('heur')

    name = heur.heur(filename[:-4], name)

    heurpath = fldr + '/' + name + '_physio'
    # for ext in ['.tsv.gz', '.json', '.log']:
    #     move_file(outfile, heurpath, ext)
    os.chdir(cwd)

    return heurpath


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    # Check options to make them internally coherent
    # #!# This can probably be done while parsing?
    # #!# Make filename check better somehow.
    options.indir = check_input_dir(options.indir)
    options.outdir = check_input_dir(options.outdir)
    options.filename = check_input_ext(options.filename, '.acq')
    ftype = 'acq'
    if not os.path.isfile(os.path.join(options.indir, options.filename)):
        options.filename = check_input_ext(options.filename[:-4], '.txt')
        ftype = 'txt'

    # #!# Change this to cases of and better message
    print('File extension is .' + ftype)

    if options.heur_file:
        options.heur_file = check_input_ext(options.heur_file, '.py')

    infile = options.indir + '/' + options.filename
    outfile = options.outdir + '/' + options.filename[:-4]

    check_file_exists(infile)
    print('File exists')

    # Read infos from file
    if ftype == 'acq':
        from bioread import read_file

        data = read_file(infile).channels
        print_info_acq(options.filename, data)
    elif ftype == 'txt':
        header = print_info_txt(options.filename)

    # If file has to be processed, process it
    if not options.info:
        if options.heur_file and options.sub:
            check_file_exists(options.heur_file)
            print(f'Preparing BIDS output using {options.heur_file}')
            outfile = use_heuristic(options.heur_file, options.sub,
                                    options.ses, options.filename,
                                    options.outdir)
        elif options.heur_file and not options.sub:
            print(f'While "-heur" was specified, option "-sub" was not.\n'
                  f'Skipping BIDS formatting.')

        # #!# Get option of no trigger! (which is wrong practice or Respiract)
        print('Reading trigger data and time index')
        if ftype == 'acq':
            trigger = data[options.chtrig].data
            time = data[options.chtrig].time_index
        elif ftype == 'txt':
            # Read full file and extract right lines.
            data = np.genfromtxt(options.filename, skip_header=HEADERLENGTH)
            trigger = data[:, options.chtrig+1]
            time = data[:, 0]

        print('Counting trigger points')
        trigger_deriv = np.diff(trigger)
        tps = trigger_deriv > options.thr
        num_tps_found = tps.sum()
        time_offset = time[tps.argmax()]

        if options.num_tps_expected:
            print('Checking number of tps')
            if num_tps_found > options.num_tps_expected:
                tps_extra = num_tps_found - options.num_tps_expected
                print('Found ' + str(tps_extra) + ' tps more than expected!\n',
                      'Assuming extra tps are at the end (try again with a ',
                      'more conservative thr)')
            elif num_tps_found < options.num_tps_expected:
                tps_missing = options.num_tps_expected - num_tps_found
                print('Found ' + str(tps_missing) + ' tps less than expected!')
                if options.tr:
                    print('Correcting time offset, assuming missing tps'
                          'are at the beginning')
                    # time_offset = time_offset - (tps_missing * options.tr)
                    time_offset = time[tps.argmax()] - (tps_missing * options.tr)
                else:
                    print('Can\'t correct time offset, (try again specifying',
                          'tr or with a more liberal thr')

            else:
                print('Found just the right amount of tps!')

        else:
            print('Not checking the number of tps')

        time = time - time_offset
        # time = data[options.chtrig].time_index - time_offset

        path_exists_or_make_it(options.outdir)

        def time2ntr(x):
            return x / options.tr

        def ntr2time(x):
            return x * options.tr

        thrline = np.ones(time.shape) * options.thr
        fig = plt.figure(figsize=FIGSIZE, dpi=SET_DPI)
        subplot = fig.add_subplot(211)
        subplot.set_title('trigger and time')
        subplot.set_ylim([-0.2, options.thr*10])
        subplot.plot(time, trigger, '-', time, thrline, 'r-.', time, time, '-')
        subplot = fig.add_subplot(223)
        subplot.set_xlim([-options.tr*4, options.tr*4])
        subplot.set_ylim([-0.2, options.thr*3])
        subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
        subplot.plot(time, trigger, '-', time, time, '-')
        subplot = fig.add_subplot(224)
        subplot.set_xlim([options.tr*(options.num_tps_expected-4), options.tr*(options.num_tps_expected+4)])
        subplot.set_ylim([-0.2, options.thr*3])
        subplot.secondary_xaxis('top', functions=(time2ntr, ntr2time))
        subplot.plot(time, trigger, '-', time, time, '-')
        plt.savefig(outfile + '_trigger_time.png', dpi=SET_DPI)
        plt.close()

        # #!# The following few lines could be a function on its own for use in python
        table = pd.DataFrame(index=time)

        if ftype == 'txt':
            col_names = header[1].split('\t')
            col_names[-1] = col_names[-1][:-1]

        if options.chsel:
            print('Extracting desired channels')
            for ch in options.chsel:
                if ftype == 'acq':
                    table[data[ch].name] = data[ch].data
                elif ftype == 'txt':
                    # preparing channel names from txt file
                    table[col_names[ch+1]] = data[:, ch+1]

        else:
            # #!# Needs a check on different channel frequency!
            print('Extracting all channels')
            if ftype == 'acq':
                for ch in range(0, len(data)):
                    table[data[ch].name] = data[ch].data
            elif ftype == 'txt':
                for ch in range(0, (data.shape[1]-1)):
                    table[col_names[ch+1]] = data[:, ch+1]

        print('Extracting minor informations')
        if ftype == 'acq':
            samp_freq = data[0].samples_per_second
        elif ftype == 'txt':
            freq_list = header[0].split('\t')
            samp_freq = 1 / float(freq_list[-1][:-2])

        table.index.names = ['time']
        table_width = len(table.columns)

        if options.table_header:
            if 'time' in options.table_header:
                ignored_headers = 1
            else:
                ignored_headers = 0

            n_headers = len(options.table_header)
            if table_width < n_headers - ignored_headers:
                print(f'Too many table headers specified!\n'
                      f'{options.table_header}\n'
                      f'Ignoring the last'
                      '{n_headers - table_width - ignored_headers}')
                options.table_header = options.table_header[:(table_width + ignored_headers)]
            elif table_width > n_headers - ignored_headers:
                missing_headers = n_headers - table_width - ignored_headers
                print(f'Not enough table headers specified!\n'
                      f'{options.table_header}\n'
                      f'Tailing {missing_headers} headers')
                for i in range(missing_headers):
                    options.table_header.append(f'missing n.{i+1}')

            table.columns = options.table_header[ignored_headers:]
            # #!# this should be iterative!
            if 'respiratory_CO2' in table.columns:
                print_plot(table, 'respiratory_CO2', outfile)

        print('Printing file')
        table.to_csv(outfile + '.tsv.gz', sep='\t', index=True, header=False, compression='gzip')
        # #!# Definitely needs check on samp_freq!
        print_json(outfile, samp_freq, time_offset, options.table_header)
        print_summary(options.filename, options.num_tps_expected,
                      num_tps_found, samp_freq, time_offset, outfile)


if __name__ == '__main__':
    _main()
