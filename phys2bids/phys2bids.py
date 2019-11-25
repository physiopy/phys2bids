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

import pandas as pd

from phys2bids import utils, viz
from phys2bids.cli.run import _get_parser


# #!# This is hardcoded until we find a better solution
HEADERLENGTH = 9


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
    utils.writefile(outfile, '.log', summary)


def print_json(filename, samp_freq, time_offset, table_header):
    start_time = -time_offset
    summary = dict(SamplingFrequency=samp_freq,
                   StartTime=start_time,
                   Columns=table_header)
    utils.writejson(filename, summary, indent=4, sort_keys=False)


def use_heuristic(heur_file, sub, ses, filename, outdir):
    utils.check_file_exists(heur_file)

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
    utils.path_exists_or_make_it(fldr)

    cwd = os.getcwd()
    os.chdir(outdir)

    heur = utils.load_heuristic(heur_file)
    name = heur.heur(filename[:-4], name)

    if record_label:
        recording = f'_recording-{record_label}'

    heurpath = fldr + '/' + name + recording + '_physio'
    # for ext in ['.tsv.gz', '.json', '.log']:
    #     move_file(outfile, heurpath, ext)
    os.chdir(cwd)

    return heurpath


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    # Check options to make them internally coherent
    # #!# This can probably be done while parsing?
    options.indir = utils.check_input_dir(options.indir)
    options.outdir = utils.check_input_dir(options.outdir)
    options.filename, ftype = utils.check_input_type(options.filename,
                                                     options.indir)

    if options.heur_file:
        options.heur_file = utils.check_input_ext(options.heur_file, '.py')

    infile = os.path.join(options.indir, options.filename)
    outfile = os.path.join(options.outdir, os.path.basename(options.filename[:-4]))

    # Read file!
    if ftype == 'acq':
        from phys2bids.interfaces.acq import populate_phys_input
    elif ftype == 'txt':
        raise Exception('txt not yet supported')
    else:
        raise Exception('This shouldn\'t happen, check out the last few'
                        'lines of code')

    phys_input = populate_phys_input(infile, options.chtrig)
    utils.print_info(options.filename, phys_input)

    # If file has to be processed, process it
    if not options.info:
        if options.heur_file and options.sub:
            utils.check_file_exists(options.heur_file)
            print(f'Preparing BIDS output using {options.heur_file}')
            outfile = use_heuristic(options.heur_file, options.sub,
                                    options.ses, options.filename,
                                    options.outdir)
        elif options.heur_file and not options.sub:
            print(f'While "-heur" was specified, option "-sub" was not.\n'
                  f'Skipping BIDS formatting.')

        # #!# Get option of no trigger! (which is wrong practice or Respiract)
        phys_input.check_trigger_amount(options.thr, options.num_tps_expected,
                                        options.tr)

        utils.path_exists_or_make_it(options.outdir)

        viz.plot_trigger(phys_input.timeseries[0], phys_input.timeseries[1],
                         outfile, options)

        #####
        ###
        # #!# This part has to become the "output object" population

        # Check how many different frequencies there are in the input
        # Create a dictionary that has one entry per frequence
        # Create an output object per entry


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
                    table[col_names[ch + 1]] = data[:, ch + 1]

        else:
            # #!# Needs a check on different channel frequency!
            print('Extracting all channels')
            if ftype == 'acq':
                for ch in range(0, len(data)):
                    table[data[ch].name] = data[ch].data
            elif ftype == 'txt':
                for ch in range(0, (data.shape[1] - 1)):
                    table[col_names[ch + 1]] = data[:, ch + 1]

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
                      f'Ignoring the last '
                      f'{n_headers - table_width - ignored_headers}')
                options.table_header = options.table_header[:(table_width + ignored_headers)]
            elif table_width > n_headers - ignored_headers:
                missing_headers = n_headers - table_width - ignored_headers
                print(f'Not enough table headers specified!\n'
                      f'{options.table_header}\n'
                      f'Tailing {missing_headers} headers')
                for i in range(missing_headers):
                    options.table_header.append(f'missing n.{i+1}')

            table.columns = options.table_header[ignored_headers:]
            # #!# Here the function viz.plot_channel should be called for the desired channels.

        print('Printing file')
        table.to_csv(outfile + '.tsv.gz', sep='\t', index=True, header=False, compression='gzip')
        # #!# Definitely needs check on samp_freq!
        print_json(outfile, samp_freq, time_offset, options.table_header)
        print_summary(options.filename, options.num_tps_expected,
                      num_tps_found, samp_freq, time_offset, outfile)


if __name__ == '__main__':
    _main()
