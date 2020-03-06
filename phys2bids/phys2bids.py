#!/usr/bin/env python3

"""
Phys2bids is a python3 library meant to set physiological files in BIDS
standard.

It was born for Acqknowledge files (BIOPAC), and at the moment it supports
``.acq`` files and ``.txt`` files obtained by labchart (ADInstruments).

It requires python 3.6 or above, as well as the modules:
- `numpy`
- `matplotlib`

In order to process ``.acq`` files, it needs `bioread`, an excellent module
that can be found at `this link`_

The project is under development.

At the very moment, it assumes:
-  the input file is from one individual scan, not one session with multiple scans.

.. _this link:
   https://github.com/uwmadison-chm/bioread

Copyright 2019, The Phys2BIDS community.
Please scroll to bottom to read full license.

"""

import os
import logging
import datetime

from copy import deepcopy
from numpy import savetxt
from pathlib import Path

from phys2bids import utils, viz, _version
from phys2bids.cli.run import _get_parser
from phys2bids.physio_obj import BlueprintOutput

LGR = logging.getLogger(__name__)


def print_summary(filename, ntp_expected, ntp_found, samp_freq, time_offset, outfile):
    """
    Prints a summary onscreen and in file with informations on the files.

    Parameters
    ----------
    filename: str
        Name of the input of phys2bids.
    ntp_expected: int
        Number of expected timepoints, as defined by user.
    ntp_found: int
        Number of timepoints found with the automatic process.
    samp_freq: float
        Frequency of sampling for the output file.
    time_offset: float
        Difference between beginning of file and first TR.
    outfile: str or path
        Fullpath to output file.

    Notes
    -----
    Outcome:
    summary: str
        Prints the summary on screen
    outfile: .log file
        File containing summary
    """
    start_time = -time_offset
    summary = (f'\n------------------------------------------------\n'
               f'Filename:            {filename}\n'
               f'\n'
               f'Timepoints expected: {ntp_expected}\n'
               f'Timepoints found:    {ntp_found}\n'
               f'Sampling Frequency:  {samp_freq} Hz\n'
               f'Sampling started at: {start_time} s\n'
               f'Tip: Time 0 is the time of first trigger\n'
               f'------------------------------------------------\n')
    LGR.info(summary)
    utils.writefile(outfile, '.log', summary)


def print_json(outfile, samp_freq, time_offset, ch_name):
    """
    Prints the json required by BIDS format.

    Parameters
    ----------
    outfile: str or path
        Fullpath to output file.
    samp_freq: float
        Frequency of sampling for the output file.
    time_offset: float
        Difference between beginning of file and first TR.
    ch_name: list of str
        List of channel names, as specified by BIDS format.

    Notes
    -----
    Outcome:
    outfile: .json file
        File containing information for BIDS.
    """
    start_time = -time_offset
    summary = dict(SamplingFrequency=samp_freq,
                   StartTime=start_time,
                   Columns=ch_name)
    utils.writejson(outfile, summary, indent=4, sort_keys=False)


def use_heuristic(heur_file, sub, ses, filename, outdir, record_label=''):
    utils.check_file_exists(heur_file)
    """
    Import the heuristic file specified by the user and uses its output
    to rename the file.

    Parameters
    ----------
    heur_file: path
        Fullpath to heuristic file.
    sub: str or int
        Name of subject.
    ses: str or int or None
        Name of session.
    filename: path
        Name of the input of phys2bids.
    outdir: str or path
        Path to the directory that will become the "site" folder
        ("root" folder of BIDS database).
    record_label: str
        Optional label for the "record" entry of BIDS.

    Returns
    -------
    heurpath: str or path
        Returned fullpath to tsv.gz new file (post BIDS formatting).
    """

    if sub[:4] != 'sub-':
        name = f'sub-{sub}'
    else:
        name = sub

    fldr = os.path.join(outdir, name)

    if ses:
        if ses[:4] != 'ses-':
            ses = f'ses-{ses}'

        fldr = os.path.join(fldr, ses)
        name = f'{name}_{ses}'

    fldr = os.path.join(fldr, 'func')
    utils.path_exists_or_make_it(fldr)

    cwd = os.getcwd()
    os.chdir(outdir)

    heur = utils.load_heuristic(heur_file)
    name = heur.heur(Path(filename).stem, name)

    recording = ''
    if record_label:
        recording = f'_recording-{record_label}'

    heurpath = os.path.join(fldr, f'{name}{recording}_physio')
    # for ext in ['.tsv.gz', '.json', '.log']:
    #     move_file(outfile, heurpath, ext)
    os.chdir(cwd)

    return heurpath


def _main(argv=None):
    """
    Main workflow of phys2bids.
    Runs the parser, does some checks on input, then imports
    the right interface file to read the input. If only info is required,
    it returns a summary onscreen.
    Otherwise, it operates on the input to return a .tsv.gz file, possibily
    in BIDS format.

    Raises
    ------
    NotImplementedError
        If the file extension is not supported yet.

    """
    options = _get_parser().parse_args(argv)

    # Check options to make them internally coherent pt. I
    # #!# This can probably be done while parsing?
    options.outdir = utils.check_input_dir(options.outdir)
    utils.path_exists_or_make_it(options.outdir)

    # Create logfile name
    basename = 'phys2bids_'
    extension = 'tsv'
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    logname = os.path.join(options.outdir, (basename + isotime + '.' + extension))

    # Set logging format
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    if options.quiet:
        logging.basicConfig(level=logging.WARNING,
                            handlers=[log_handler, sh])
    elif options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            handlers=[log_handler, sh])
    else:
        logging.basicConfig(level=logging.INFO,
                            handlers=[log_handler, sh])

    version_number = _version.get_versions()['version']
    LGR.info(f'Currently running phys2bids version {version_number}')
    LGR.info(f'Input file is {options.filename}')

    # Check options to make them internally coherent pt. II
    # #!# This can probably be done while parsing?
    options.indir = utils.check_input_dir(options.indir)
    options.filename, ftype = utils.check_input_type(options.filename,
                                                     options.indir)

    if options.heur_file:
        options.heur_file = utils.check_input_ext(options.heur_file, '.py')
        utils.check_file_exists(options.heur_file)

    infile = os.path.join(options.indir, options.filename)
    utils.check_file_exists(infile)
    outfile = os.path.join(options.outdir,
                           os.path.splitext(os.path.basename(options.filename))[0])

    # Read file!
    if ftype == 'acq':
        from phys2bids.interfaces.acq import populate_phys_input
    elif ftype == 'txt':
        from phys2bids.interfaces.txt import populate_phys_input
    else:
        # #!# We should add a logger here.
        raise NotImplementedError('Currently unsupported file type.')

    LGR.info(f'Reading the file {infile}')
    phys_in = populate_phys_input(infile, options.chtrig)
    LGR.info('Reading infos')
    phys_in.print_info(options.filename)
    # #!# Here the function viz.plot_channel should be called
    if options.chplot != '' or options.info:
        viz.plot_all(phys_in, infile, options.chplot)
    # If only info were asked, end here.
    if options.info:
        return

    # Run analysis on trigger channel to get first timepoint and the time offset.
    # #!# Get option of no trigger! (which is wrong practice or Respiract)
    phys_in.check_trigger_amount(options.chtrig, options.thr, options.num_timepoints_expected,
                                 options.tr)

    # Create trigger plot. If possible, to have multiple outputs in the same
    # place, adds sub and ses label.
    LGR.info('Plot trigger')
    plot_path = deepcopy(outfile)
    if options.sub:
        plot_path += f'_sub-{options.sub}'
    if options.ses:
        plot_path += f'_sub-{options.ses}'
    viz.plot_trigger(phys_in.timeseries[0], phys_in.timeseries[options.chtrig],
                     plot_path, options)

    # The next few lines remove the undesired channels from phys_in.
    if options.chsel:
        LGR.info('Dropping unselected channels')
        for i in reversed(range(0, phys_in.ch_amount)):
            if i not in options.chsel:
                phys_in.delete_at_index(i)

    # If requested, change channel names.
    if options.ch_name:
        LGR.info('Renaming channels with given names')
        phys_in.rename_channels(options.ch_name)

    # The next few lines create a dictionary of different BlueprintInput
    # objects, one for each unique frequency in phys_in
    uniq_freq_list = set(phys_in.freq)
    output_amount = len(uniq_freq_list)
    if output_amount > 1:
        LGR.warning(f'Found {output_amount} different frequencies in input!')

    LGR.info(f'Preparing {output_amount} output files.')
    phys_out = {}  # create phys_out dict that will have a
    # blueprint object per frequency
    # for each different frequency
    for uniq_freq in uniq_freq_list:
        # copy the phys_in object to the new dict entry
        phys_out[uniq_freq] = deepcopy(phys_in)
        # this counter will take into account how many channels are eliminated
        count = 0
        # for each channel in the original phys_in object
        # take the frequency
        for idx, i in enumerate(phys_in.freq):
            # if that frequency is different than the frequency of the phys_obj entry
            if i != uniq_freq:
                # eliminate that channel from the dict since we only want channels
                # with the same frequency
                phys_out[uniq_freq].delete_at_index(idx - count)
                # take into acount the elimination so in the next eliminated channel we
                # eliminate correctly
                count += 1
        # Also create a BlueprintOutput object for each unique frequency found.
        # Populate it with the corresponding blueprint input and replace it
        # in the dictionary.
        phys_out[uniq_freq] = BlueprintOutput.init_from_blueprint(phys_out[uniq_freq])
    if options.heur_file and options.sub:
        LGR.info(f'Preparing BIDS output using {options.heur_file}')
    elif options.heur_file and not options.sub:
        LGR.warning(f'While "-heur" was specified, option "-sub" was not.\n'
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

        LGR.info(f'Exporting files for freq {uniq_freq}')
        savetxt(outfile + '.tsv.gz', phys_out[uniq_freq].timeseries,
                fmt='%.8e', delimiter='\t')
        print_json(outfile, phys_out[uniq_freq].freq,
                   phys_out[uniq_freq].start_time,
                   phys_out[uniq_freq].ch_name)
        print_summary(options.filename, options.num_timepoints_expected,
                      phys_in.num_timepoints_found, uniq_freq,
                      phys_out[uniq_freq].start_time, outfile)


if __name__ == '__main__':
    _main()

"""
Copyright 2019, The Phys2BIDS community.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
