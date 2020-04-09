#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A parallel CLI utility to segment the physiological input files.

Cuts the physiological recording files into multiple runs
with padding at start and end

"""

import datetime
import logging
import os
# from copy import deepcopy
# from pathlib import Path

from numpy import ones

from phys2bids import utils
from phys2bids.cli.split import _get_parser
from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)


def split2phys(filename, info=False, indir='.', outdir='.', chtrig=1,
               ntp_list=[0, ], tr_list=[1, ], thr=None, padding=0):
    """

    Parallel workflow of phys2bids.

    Runs the split parser, does some check on inputs and exports
    end indexes of each run based on npt_list and tr_list

    Arguments
    ---------

    Returns
    --------
        ...
    """
    outdir = utils.check_input_dir(outdir)
    utils.path_exists_or_make_it(outdir)

    # Create logfile name
    basename = 'split2phys_'
    extension = 'tsv'
    isotime = datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')
    logname = os.path.join(outdir, (basename + isotime + '.' + extension))

    # Set logging format
    log_formatter = logging.Formatter(
        '%(asctime)s\t%(name)-12s\t%(levelname)-8s\t%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S')

    # Set up logging file and open it for writing
    log_handler = logging.FileHandler(logname)
    log_handler.setFormatter(log_formatter)
    sh = logging.StreamHandler()

    logging.basicConfig(level=logging.INFO,
                        handlers=[log_handler, sh])

    version_number = _version.get_versions()['version']
    LGR.info(f'Currently running split2phys version {version_number}')
    LGR.info(f'Input file is {filename}')

    # Check options to make them internally coherent pt. II
    # #!# This can probably be done while parsing?
    indir = utils.check_input_dir(indir)
    filename, ftype = utils.check_input_type(filename,
                                             indir)

    infile = os.path.join(indir, filename)
    utils.check_file_exists(infile)

    # Check that ntp_list is longer than 1 element
    # If/when we set other parameters, we're going to change here
    if len(ntp_list) == 1:
        raise Exception('Only one run was specified. Don\'t run this workflow, '
                        'or check input')

    # Check equivalent length of list_ntp and list_tr
    if len(tr_list) != 1 and len(ntp_list) != len(tr_list):
        # Check out this page for all the builtin errors:
        # https://docs.python.org/3/library/exceptions.html#bltin-exceptions

    # Import right interface to read the file
    if ftype == 'acq':
        from phys2bids.interfaces.acq import populate_phys_input
    elif ftype == 'txt':
        from phys2bids.interfaces.txt import populate_phys_input
    else:
        # #!# We should add a logger here.
        raise NotImplementedError('Currently unsupported file type.')

    # Actually read file!
    LGR.info(f'Reading the file {infile}')
    phys_in = populate_phys_input(infile, chtrig)  # phys_in is a BlueprintInput object
    LGR.info('Reading infos')
    phys_in.print_info(filename)

    if chplot != '' or info:
        viz.plot_all(phys_in.ch_name, phys_in.timeseries, phys_in.units,
                     phys_in.freq, infile, chplot)
    # If only info were asked, end here.
    if info:
        return

    if len(tr_list) == 1:
        tr_list = tr_list * ones(len(ntp_list))

    # Sum of values in ntp_list should be equivalent to num_timepoints_found
    phys_in.check_trigger_amount(chtrig=chtrig, thr=thr,
                                 num_timepoints_expected=sum(ntp_list),
                                 tr=1)

    # Check that sum(ntp_list) is equivalent to num_timepoints_found, else bye!
    # num_timepoints_found becomes an attribute of the object when you call check_trigger_amount
    if phys_in.num_timepoints_found != sum(ntp_list):
        raise ValueError()  # not sure if it's the good one

    # Initialize dictionaries to save phys_in endpoints
    run_endpoints = {}

    # initialise start index as 0
    start_index = 0

    for run_idx, run_tps in enumerate(list_ntp):
        # ascertain run length and initialise Blueprint object
        phys_in.check_trigger_amount(ntp=run_tps, tr=list_tr[run_idx])

        # define padding - 20s * freq of trigger - padding is in nb of samples
        padding = 20 * phys_in.freq[chtrig]

        # LET'S START NOT SUPPORTING MULTIFREQ - start_index is first elem of tuple
        end_index = run_tps * list_tr[run_idx] * phys_in.freq[chtrig] + \
            start_index + phys_in.trig_idx

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[chtrig].shape[0] < (end_index + padding):
            padding = phys_in.timeseries[chtrig].shape[0] - end_index

        # Save end_index in dictionary -> start_index is run_idx-1
        # While saving, add the padding
        run_endpoints[run_idx] = (end_index + padding)

        # set start_index for next run as end_index of this one
        start_index = end_index

    # make dict exportable
    # or call it from phys2bids
    # or call phys2bids from here
    # or integrate this bit of code in phys2bids and adapt main parser by accepting
    # lists and adding -run argument


def _main(argv=None):

    options = _get_parser().parse_args(argv)
    split2phys(**vars(options))


if __name__ == '__main__':
    _main()
