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

from copy import deepcopy
from numpy import savetxt

from phys2bids import utils, viz
from phys2bids.cli.run import _get_parser
from phys2bids.physio_obj import blueprint_output


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


def print_json(filename, samp_freq, time_offset, ch_name):
    start_time = -time_offset
    summary = dict(SamplingFrequency=samp_freq,
                   StartTime=start_time,
                   Columns=ch_name)
    utils.writejson(filename, summary, indent=4, sort_keys=False)


def use_heuristic(heur_file, sub, ses, filename, outdir, record_label=''):
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
        utils.check_file_exists(options.heur_file)

    infile = os.path.join(options.indir, options.filename)
    utils.check_file_exists(infile)
    outfile = os.path.join(options.outdir, os.path.basename(options.filename[:-4]))

    # Read file!
    if ftype == 'acq':
        from phys2bids.interfaces.acq import populate_phys_input
    elif ftype == 'txt':
        raise Exception('txt not yet supported')
    else:
        raise Exception('This shouldn\'t happen, check out the last few '
                        'lines of code')

    print('Reading the file')
    phys_in = populate_phys_input(infile, options.chtrig)
    print('Reading infos')
    utils.print_info(options.filename, phys_in)
    # #!# Here the function viz.plot_channel should be called
    # for the desired channels.

    # If file has to be processed, process it
    if not options.info:

        # #!# Get option of no trigger! (which is wrong practice or Respiract)
        phys_in.check_trigger_amount(options.thr, options.num_tps_expected,
                                     options.tr)
        print('Checking that the output folder exists')
        utils.path_exists_or_make_it(options.outdir)
        print('Plot trigger')
        viz.plot_trigger(phys_in.timeseries[0], phys_in.timeseries[1],
                         outfile, options)

        # The next few lines remove the undesired channels from phys_in.
        if options.chsel:
            print('Dropping unselected channels')
            for i in [x for x in reversed(range(0, phys_in.ch_amount))
                      if x not in options.chsel]:
                phys_in.delete_at_index(i)

        # If requested, change channel names.
        if options.ch_name:
            print('Renaming channels with given names')
            phys_in.rename_channels(options.ch_name)

        # The next few lines create a dictionary of different blueprint_input
        # objects, one for each unique frequency in phys_in
        uniq_freq_list = set(phys_in.freq)
        print(f'Found {len(uniq_freq_list)} unique frequencies.')
        phys_out = {}
        for uniq_freq in uniq_freq_list:
            phys_out[uniq_freq] = deepcopy(phys_in)
            for i in [i for i, x in enumerate(reversed(phys_in.freq))
                      if x != uniq_freq]:
                phys_out[uniq_freq].delete_at_index(phys_in.ch_amount-i-1)

        for uniq_freq in uniq_freq_list:
            phys_out[uniq_freq] = blueprint_output.init_from_blueprint(phys_out[uniq_freq])

        output_amount = len(uniq_freq_list)
        if output_amount > 1:
            print(f'Found {output_amount} different frequencies in input!\n'
                  f'Consequently, preparing {output_amount} of output files')

        if options.heur_file and options.sub:
            print(f'Preparing BIDS output using {options.heur_file}')
        elif options.heur_file and not options.sub:
            print(f'While "-heur" was specified, option "-sub" was not.\n'
                  f'Skipping BIDS formatting.')

        for uniq_freq in uniq_freq_list:
            # If possible, prepare bids renaming.
            if options.heur_file and options.sub:
                if output_amount > 1:
                    # Add "recording-freq" to filename if more than one freq
                    outfile = use_heuristic(options.heur_file, options.sub,
                                            options.ses, options.filename,
                                            options.outdir, uniq_freq)
                else:
                    outfile = use_heuristic(options.heur_file, options.sub,
                                            options.ses, options.filename,
                                            options.outdir)

            elif output_amount > 1:
                # Append "freq" to filename if more than one freq
                outfile = f'outfile_{uniq_freq}'

            print('Exporting files for freq {uniq_freq}')
            savetxt(outfile + '.tsv.gz', phys_out[uniq_freq].timeseries,
                    fmt='%.8e', delimiter='\t')
            print_json(outfile, phys_out[uniq_freq].freq,
                       phys_out[uniq_freq].start_time,
                       phys_out[uniq_freq].ch_name)
            print_summary(options.filename, options.num_tps_expected,
                          phys_in.num_tps_found, uniq_freq,
                          phys_out[uniq_freq].start_time, outfile)


if __name__ == '__main__':
    _main()
