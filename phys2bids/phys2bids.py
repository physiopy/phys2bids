#!/usr/bin/env python3

"""
Phys2bids is a python3 library meant to set physiological files in BIDS standard.

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

import datetime
import logging
import os
import sys
from copy import deepcopy
from shutil import copy as cp

import numpy as np

from phys2bids import utils, viz, _version, bids
from phys2bids.cli.run import _get_parser
from phys2bids.physio_obj import BlueprintOutput
from phys2bids.slice4phys import slice4phys

from . import __version__
from .due import due, Doi

LGR = logging.getLogger(__name__)


def print_summary(filename, ntp_expected, ntp_found, samp_freq, time_offset, outfile):
    """
    Print a summary onscreen and in file with informations on the files.

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
               f'Sampling started at: {start_time:.4f} s\n'
               f'Tip: Time 0 is the time of first trigger\n'
               f'------------------------------------------------\n')
    LGR.info(summary)
    utils.write_file(outfile, '.log', summary)


def print_json(outfile, samp_freq, time_offset, ch_name):
    """
    Print the json required by BIDS format.

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
                   StartTime=round(start_time, 4),
                   Columns=ch_name)
    utils.write_json(outfile, summary, indent=4, sort_keys=False)


@due.dcite(
     Doi('10.5281/zenodo.3470091'),
     path='phys2bids',
     description='Conversion of physiological trace data to BIDS format',
     version=__version__,
     cite_module=True)
@due.dcite(
    Doi('10.1038/sdata.2016.44'),
    path='phys2bids',
    description='The BIDS specification',
    cite_module=True)
def phys2bids(filename, info=False, indir='.', outdir='.', heur_file=None,
              sub=None, ses=None, chtrig=1, chsel=None, num_timepoints_expected=None,
              tr=None, thr=None, pad=9, ch_name=[], yml='', debug=False, quiet=False):
    """
    Run main workflow of phys2bids.

    Runs the parser, does some checks on input, then imports
    the right interface file to read the input. If only info is required,
    it returns a summary onscreen.
    Otherwise, it operates on the input to return a .tsv.gz file, possibly
    in BIDS format.

    Raises
    ------
    NotImplementedError
        If the file extension is not supported yet.
    """
    # Check options to make them internally coherent pt. I
    # #!# This can probably be done while parsing?
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, 'code'), exist_ok=True)
    conversion_path = os.path.join(outdir, 'code', 'conversion')
    os.makedirs(conversion_path, exist_ok=True)

    # Create logfile name
    basename = 'phys2bids_'
    extension = 'tsv'
    isotime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    logname = os.path.join(conversion_path, (basename + isotime + '.' + extension))

    # Set logging format
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    if quiet:
        logging.basicConfig(level=logging.WARNING,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    elif debug:
        logging.basicConfig(level=logging.DEBUG,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            handlers=[log_handler, sh], format='%(levelname)-10s %(message)s')

    version_number = _version.get_versions()['version']
    LGR.info(f'Currently running phys2bids version {version_number}')
    LGR.info(f'Input file is {filename}')

    # Save call.sh
    arg_str = ' '.join(sys.argv[1:])
    call_str = f'phys2bids {arg_str}'
    f = open(os.path.join(conversion_path, 'call.sh'), "a")
    f.write(f'#!bin/bash \n{call_str}')
    f.close()

    # Check options to make them internally coherent pt. II
    # #!# This can probably be done while parsing?
    indir = os.path.abspath(indir)
    if chtrig < 1:
        raise Exception('Wrong trigger channel. Channel indexing starts with 1!')

    filename, ftype = utils.check_input_type(filename,
                                             indir)

    if heur_file:
        heur_file = utils.check_input_ext(heur_file, '.py')
        utils.check_file_exists(heur_file)

    infile = os.path.join(indir, filename)
    utils.check_file_exists(infile)

    if isinstance(num_timepoints_expected, int):
        num_timepoints_expected = [num_timepoints_expected]
    if isinstance(tr, (int, float)):
        tr = [tr]

    if tr is not None and num_timepoints_expected is not None:
        # If tr and ntp were specified, check that tr is either length one or ntp.
        if len(num_timepoints_expected) != len(tr) and len(tr) != 1:
            raise Exception('Number of sequence types listed with TR '
                            'doesn\'t match expected number of runs in '
                            'the session')

    # Read file!
    LGR.info(f'Reading the file {infile}')
    if ftype == 'acq':
        from phys2bids.io import load_acq
        phys_in = load_acq(infile, chtrig)
    elif ftype == 'txt':
        from phys2bids.io import load_txt
        phys_in = load_txt(infile, chtrig)
    elif ftype == 'mat':
        from phys2bids.io import load_mat
        phys_in = load_mat(infile, chtrig)

    LGR.info('Checking that units of measure are BIDS compatible')
    for index, unit in enumerate(phys_in.units):
        phys_in.units[index] = bids.bidsify_units(unit)

    LGR.info('Reading infos')
    phys_in.print_info(filename)
    # #!# Here the function viz.plot_channel should be called
    viz.plot_all(phys_in.ch_name, phys_in.timeseries, phys_in.units,
                 phys_in.freq, infile, conversion_path)
    # If only info were asked, end here.
    if info:
        return

    # The next few lines remove the undesired channels from phys_in.
    if chsel:
        LGR.info('Dropping unselected channels')
        for i in reversed(range(0, phys_in.ch_amount)):
            if i not in chsel:
                phys_in.delete_at_index(i)

    # If requested, change channel names.
    if ch_name:
        LGR.info('Renaming channels with given names')
        phys_in.rename_channels(ch_name)

    # Checking acquisition type via user's input
    if tr is not None and num_timepoints_expected is not None:

        #  Multi-run acquisition type section
        #  Check list length, more than 1 means multi-run
        if len(num_timepoints_expected) > 1:
            # if multi-run of same sequence type, pad list with ones
            # and multiply array with user's input
            if len(tr) == 1:
                tr = np.ones(len(num_timepoints_expected)) * tr[0]

            # Sum of values in ntp_list should be equivalent to num_timepoints_found
            phys_in.check_trigger_amount(thr=thr,
                                         num_timepoints_expected=sum(num_timepoints_expected),
                                         tr=1)

            # Check that sum of tp expected is equivalent to num_timepoints_found,
            # if it passes call slice4phys
            if phys_in.num_timepoints_found != sum(num_timepoints_expected):
                raise Exception('The number of triggers found is different '
                                'than expected. Better stop now than break '
                                'something.')

            # slice the recording based on user's entries
            # !!! ATTENTION: PHYS_IN GETS OVERWRITTEN AS DICTIONARY
            phys_in = slice4phys(phys_in, num_timepoints_expected, tr,
                                 phys_in.thr, pad)
            # returns a dictionary in the form {run_idx: phys_in[startpoint, endpoint]}

            # save a figure for each run | give the right acquisition parameters for runs
            fileprefix = os.path.join(conversion_path,
                                      os.path.splitext(os.path.basename(filename))[0])
            for i, run in enumerate(phys_in.keys()):
                plot_fileprefix = f'{fileprefix}_0{run}'
                viz.export_trigger_plot(phys_in[run], chtrig, plot_fileprefix, tr[i],
                                        num_timepoints_expected[i], filename,
                                        sub, ses)

        # Single run acquisition type, or : nothing to split workflow
        else:
            # Run analysis on trigger channel to get first timepoint
            # and the time offset.
            phys_in.check_trigger_amount(thr, num_timepoints_expected[0], tr[0])
            # save a figure of the trigger
            fileprefix = os.path.join(conversion_path,
                                      os.path.splitext(os.path.basename(filename))[0])
            viz.export_trigger_plot(phys_in, chtrig, fileprefix, tr[0],
                                    num_timepoints_expected[0], filename,
                                    sub, ses)

            # Reassign phys_in as dictionary
            # !!! ATTENTION: PHYS_IN GETS OVERWRITTEN AS DICTIONARY
            phys_in = {1: phys_in}

    else:
        LGR.warning('Skipping trigger pulse count. If you want to run it, '
                    'call phys2bids using both "-ntp" and "-tr" arguments')
        # !!! ATTENTION: PHYS_IN GETS OVERWRITTEN AS DICTIONARY
        phys_in = {1: phys_in}

    # The next few lines create a dictionary of different BlueprintInput
    # objects, one for each unique frequency for each run in phys_in
    # they also save the amount of runs and unique frequencies
    run_amount = len(phys_in)
    uniq_freq_list = set(phys_in[1].freq)
    freq_amount = len(uniq_freq_list)
    if freq_amount > 1:
        LGR.info(f'Found {freq_amount} different frequencies in input!')

    if run_amount > 1:
        LGR.info(f'Found {run_amount} different scans in input!')

    LGR.info(f'Preparing {freq_amount*run_amount} output files.')
    # Create phys_out dict that will have a blueprint object for each different frequency
    phys_out = {}

    if heur_file is not None and sub is not None:
        LGR.info(f'Preparing BIDS output using {heur_file}')
        # If heuristics are used, init a dict of arguments to pass to use_heuristic
        heur_args = {'heur_file': heur_file, 'sub': sub, 'ses': ses,
                     'filename': filename, 'outdir': outdir, 'run': '',
                     'record_label': ''}
        # Generate participants.tsv file if it doesn't exist already.
        # Update the file if the subject is not in the file.
        # Do not update if the subject is already in the file.
        bids.participants_file(outdir, yml, sub)
        # Generate dataset_description.json file if it doesn't exist already.
        bids.dataset_description_file(outdir)
        # Generate README file if it doesn't exist already.
        bids.readme_file(outdir)
        cp(heur_file, os.path.join(conversion_path,
           os.path.splitext(os.path.basename(heur_file))[0] + '.py'))
    elif heur_file is not None and sub is None:
        LGR.warning('While "-heur" was specified, option "-sub" was not.\n'
                    'Skipping BIDS formatting.')

    # Export a (set of) phys_out for each element in phys_in
    # run keys start from 1 (human friendly)
    for run in phys_in.keys():
        for uniq_freq in uniq_freq_list:
            # Initialise the key for the (possibly huge amount of) dictionary entries
            key = f'{run}_{uniq_freq}'
            # copy the phys_in object to the new dict entry
            phys_out[key] = deepcopy(phys_in[run])
            # this counter will take into account how many channels are eliminated
            count = 0
            # for each channel in the original phys_in object
            # take the frequency
            for idx, i in enumerate(phys_in[run].freq):
                # if that frequency is different than the frequency of the phys_obj entry
                if i != uniq_freq:
                    # eliminate that channel from the dict since we only want channels
                    # with the same frequency
                    phys_out[key].delete_at_index(idx - count)
                    # take into acount the elimination so in the next eliminated channel we
                    # eliminate correctly
                    count += 1
            # Also create a BlueprintOutput object for each unique frequency found.
            # Populate it with the corresponding blueprint input and replace it
            # in the dictionary.
            # Add time channel in the proper frequency.
            if uniq_freq != phys_in[run].freq[0]:
                phys_out[key].ch_name.insert(0, phys_in[run].ch_name[0])
                phys_out[key].units.insert(0, phys_in[run].units[0])
                phys_out[key].timeseries.insert(0, np.linspace(phys_in[run].timeseries[0][0],
                                                phys_in[run].timeseries[0][-1],
                                                num=phys_out[key].timeseries[0].shape[0]))
            # Add trigger channel in the proper frequency.
            if uniq_freq != phys_in[run].freq[chtrig]:
                phys_out[key].ch_name.insert(1, phys_in[run].ch_name[chtrig])
                phys_out[key].units.insert(1, phys_in[run].units[chtrig])
                phys_out[key].timeseries.insert(1, np.interp(phys_out[key].timeseries[0],
                                                             phys_in[run].timeseries[0],
                                                             phys_in[run].timeseries[chtrig]))
            phys_out[key] = BlueprintOutput.init_from_blueprint(phys_out[key])

        # Preparing output parameters: name and folder.
        for uniq_freq in uniq_freq_list:
            key = f'{run}_{uniq_freq}'
            # If possible, prepare bids renaming.
            if heur_file is not None and sub is not None:
                # Add run info to heur_args if more than one run is present
                if run_amount > 1:
                    heur_args['run'] = f'{run:02d}'

                # Append "recording-freq" to filename if more than one freq
                if freq_amount > 1:
                    heur_args['record_label'] = f'{uniq_freq:.0f}Hz'

                phys_out[key].filename = bids.use_heuristic(**heur_args)

                # If any filename exists already because of multirun, append labels
                # But warn about the non-validity of this BIDS-like name.
                if run_amount > 1:
                    if any([phys.filename == phys_out[key].filename
                           for phys in phys_out.values()]):
                        phys_out[key].filename = (f'{phys_out[key].filename}'
                                                  f'_take-{run}')
                        LGR.warning('Identified multiple outputs with the same name.\n'
                                    'Appending fake label to avoid overwriting.\n'
                                    '!!! ATTENTION !!! the output is not BIDS compliant.\n'
                                    'Please check heuristics to solve the problem.')

            else:
                phys_out[key].filename = os.path.join(outdir,
                                                      os.path.splitext(os.path.basename(filename)
                                                                       )[0])
                # Append "run" to filename if more than one run
                if run_amount > 1:
                    phys_out[key].filename = f'{phys_out[key].filename}_{run:02d}'
                # Append "freq" to filename if more than one freq
                if freq_amount > 1:
                    phys_out[key].filename = f'{phys_out[key].filename}_{uniq_freq:.0f}Hz'

            LGR.info(f'Exporting files for run {run} freq {uniq_freq}')
            np.savetxt(phys_out[key].filename + '.tsv.gz',
                       phys_out[key].timeseries, fmt='%.8e', delimiter='\t')
            print_json(phys_out[key].filename, phys_out[key].freq,
                       phys_out[key].start_time, phys_out[key].ch_name)
            print_summary(filename, num_timepoints_expected,
                          phys_in[run].num_timepoints_found, uniq_freq,
                          phys_out[key].start_time,
                          os.path.join(conversion_path,
                                       os.path.splitext(os.path.basename(phys_out[key].filename)
                                                        )[0]))


def _main(argv=None):
    options = _get_parser().parse_args(argv)
    phys2bids(**vars(options))


if __name__ == '__main__':
    _main(sys.argv[1:])

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
