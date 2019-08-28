import os
import argparse
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from bioread import read_file

VERSION = '3.0.0'


def _version_():
    print('physiobids v.' + VERSION)


def check_input_dir(indir):
    if indir[-1:] == '/':
        indir = indir[-1:]

    return indir


def check_input_ext(file, ext):
    if file[-4:] != ext:
        file = file + ext

    return file


def check_file_exists(file):
    """
    Check if file exists.
    """
    if not os.path.isfile(file) and file is not None:
        print('The file' + file + 'does not exist!')
        sys.exit()


def _get_parser():
    """
    Parses command line inputs for this function

    Returns
    -------
    parser.parse_args() : argparse dict

    """
    parser = argparse.ArgumentParser()
    # Argument parser follow template provided by RalphyZ, also used by tedana.
    # https://stackoverflow.com/a/43456577
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required Argument:')
    required.add_argument('-in', '--input-file',
                          dest='filename',
                          type=str,
                          help=('The name of the acq file, with or without ',
                                'extension.   Must be an .acq file!'),
                          required=True)
    optional.add_argument('-info','--info',
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
                          help=('Folder where output should be placed. ',
                                'If \"-heur\" is used, it\'ll become ',
                                'the site folder. Requires \"-sub\",',
                                ' and it\'s possible to specify \"-ses\""'),
                          default='.')
    optional.add_argument('-heur', '--heuristic',
                          dest='heur',
                          type=str,
                          help=('File containing heuristic, with or without ',
                                'extension. Specify path to it if necessary.'),
                          default='heur.py')
    optional.add_argument('-sub', '--subject',
                          dest='sub',
                          type=str,
                          help=('To be specified with \"-heur\". Code of ',
                                'subject to process.',
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-ses', '--session',
                          dest='ses',
                          type=str,
                          help=('To be specified with \"-heur\". Code of ',
                                'session to process.',
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-chtrig', '--channel-trigger',
                          dest='chtrig',
                          type=int,
                          help=('The number corresponding to the trigger channel.',
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
                          default=['time', 'respiratory_chest', 'trigger', 'cardiac',
                                   'respiratory_CO2', 'respiratory_O2'])  # #!# Has to go to empty list
    optional.add_argument('-v', '--version', action='version', version=('%(prog)s ' + VERSION))

    parser._action_groups.append(optional)

    return parser


def writefile(filename, ext, text):
    with open(filename + ext, 'w') as text_file:
        print('{}'.format(text), text_file)


def print_info(filename, data):
    print('File ' + filename + ' contains:\n')
    for ch in range(0, len(data)):
         print(str(ch) + ': ' + data[ch].name)


def print_summary(filename, ntp_expected, ntp_found, samp_freq, start_time, outfile):
    summary = ('------------------------------------------------\n',
               'Filename:            ' + filename + '.acq\n',
               '\n',
               'Timepoints expected: ' + ntp_expected + '\n',
               'Timepoints found:    ' + ntp_found + '\n',
               'Sampling Frequency:  ' + samp_freq + ' Hz\n',
               'Sampling started at: ' + start_time + ' s\n',
               'Tip: Time 0 is the time of first trigger\n',
               '------------------------------------------------\n')
    print(summary)
    writefile(outfile, '.log', summary)


def print_json(filename, samp_freq, start_time, table_header):
    summary = ('{\n',
               '\t\"SamplingFrequency\": ' + samp_freq + '\n',
               '\t\"StartTime\": ' + start_time + '\n',
               '\t\"Columns\": ' + str(table_header) + '\n',
               '}') # check table header
    writefile(filename, '.json', summary)


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    # Check options to make coherent internally
    # #!# This can probably be done while parsing?
    options.indir = check_input_dir(options.indir)
    options.outdir = check_input_dir(options.outdir)
    options.filename = check_input_ext(options.filename,'.acq')

    infile = options.indir + '/' + options.filename
    outfile = options.outdir + '/' + options.filename[:-4]

    check_file_exists(infile)
    data = read_file(infile).channels
    print_info(options.filename, data)

    if not options.info:
        # #!# Get option of no trigger! (which is wrong practice)
        print('Reading trigger data and time index')
        trigger = data[options.chtrig].data
        time = data[options.chtrig].time_index

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
                    print('Correcting time offset, assuming missing tps are at the beginning')
                    # time_offset = time_offset - (tps_missing * options.tr)
                    time_offset = time[tps.argmax()] - (tps_missing * options.tr)
                else:
                    print('Can\'t correct time offset, (try again specifying',
                          'tr or with a more liberal thr')

            else:
                print('Found just the right amount of tps!')

        else:
            print('Not checking the number of tps')

        # time = time - time_offset
        time = data[options.chtrig].time_index - time_offset

        # #!# The following few lines could be a function on its own for use in python
        table = pd.DataFrame(index=time)

        if options.chsel:
            print('Extracting desired channels')
            for ch in options.chsel:
                table[data[ch].name] = data[ch].data

        else:
            # #!# Needs a check on different channel frequency!
            print('Extracting all channels')
            for ch in range(0, len(data)):
                table[data[ch].name] = data[ch].data

        table.index.names = ['time']
        n_cols = len(table.columns)

        if options.table_header:
            if 'time' in options.table_header:
                ignored_header = 1
            else:
                ignored_header = 0

            if n_cols + ignored_header < len(options.table_header):
                options.table_header = options.table_header[:(n_cols + ignored_header)]

            table.columns = options.table_header[ignored_header:]

        table.to_csv('BH4.tsv.gzip', sep='\t', index=True, header=False, compression='gzip')
        # Definitely needs check on samp_freq!
        print_json(outfile, data[0].samples_per_second, time_offset, options.table_header)
        print_summary(options.filename, options.num_tps_expected, num_tps_found, data[0].samples_per_second, time_offset, outfile)


if __name__ == '__main__':
    _main()
