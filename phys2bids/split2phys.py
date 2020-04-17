#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

A parallel to phys2bids.

Cuts the physiological recording files into multiple runs
with padding at start and end

"""

import datetime
import logging
import os
# from copy import deepcopy
# from pathlib import Path

from phys2bids import utils, viz, _version
from phys2bids.cli.split import _get_parser
# from phys2bids.physio_obj import

LGR = logging.getLogger(__name__)


def ses2run(filename, info=False, indir='.', outdir='.', chtrig=1,
               ntp_list=[0, ], tr_list=[1, ], chplot='', thr=None, padding=0):
    """

    Parallel workflow of phys2bids.

    Runs the split parser, does some check on inputs and exports
    end indexes of each run based on npt_list and tr_list

    It could be a function in phys
    uses if it detects lists in tr and ntp arguments

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

    # Check equivalency of length for list_ntp and list_tr
    if len(tr_list) != 1 and len(ntp_list) < len(tr_list):
        raise Exception('Multiple sequence types have been listed in tr,'
                        'but the number of run is less than types of sequence')
    # 2 sequence types, 3 runs ; which one is it??????
    if len(tr_list) != 1 and len(tr_list) < len(ntp_list):
        raise Exception('Multiple sequence types have been listed in tr,'
                        'but the number of run doesn\'t match')

    # Check out this page for all the builtin errors:
    # https://docs.python.org/3/library/exceptions.html#bltin-exceptions

    # if multiple runs of same sequence in recording - pad the list with same value
    if len(tr_list) == 1:
        tr_list = tr_list * len(ntp_list)

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

    # Sum of values in ntp_list should be equivalent to num_timepoints_found
    phys_in.check_trigger_amount(chtrig=chtrig, thr=thr,
                                 num_timepoints_expected=sum(ntp_list),
                                 tr=1)  # TODO : define a non-hard-coded value

    # Check that sum(ntp_list) is equivalent to num_timepoints_found, else bye!
    # num_timepoints_found becomes an attribute of the object when you call check_trigger_amount
    if phys_in.num_timepoints_found != sum(ntp_list):
        raise ValueError()  # not sure if it's the good one
        # TODO : automatize tps correction

    # Initialize dictionaries to save phys_in endpoints
    run_endpoints = {}

    # initialise start index as 0
    start_index = 0

    for run_idx, run_tps in enumerate(ntp_list):
        # ascertain run length and and (re)initialise Blueprint object
        if run_idx == 0:
            phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])
        else:
            phys_in = phys_in.delete_at_index([start_index:end_index])
            phys_in.check_trigger_amount(ntp=run_tps, tr=tr_list[run_idx])
        # define padding - 20s * freq of trigger - padding is in nb of samples
        padding = 20 * phys_in.freq[chtrig]

        # LET'S START NOT SUPPORTING MULTIFREQ - end_index is nb of samples in run+start+first_trig
        end_index = (run_tps * tr_list[run_idx]) * phys_in.freq[chtrig] + \
            start_index + phys_in.trig_idx  # problem : it only goes for the first run
        #  either we update phys_in wth delete_at_index and use this attribute and drop start_index
        #  or we don't use this attribute and figure the index another way

        # if the padding is too much for the remaining timeseries length
        # then the padding stops at the end of recording
        if phys_in.timeseries[chtrig].shape[0] < (end_index + padding):
            padding = phys_in.timeseries[chtrig].shape[0] - end_index

        # Save end_index in dictionary -> start_index is run_idx-1
        # While saving, add the padding ; or not if we can feed it to phys2bids
        run_endpoints[run_idx] = (end_index + padding)

        # set start_index for next run as end_index of this one
        # start_index = end_index

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
