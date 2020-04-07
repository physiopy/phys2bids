#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A parallel CLI utility to segment the physiological input file
into multiple runs with padding

"""

import os
import logging
import datetime

#from copy import deepcopy
#from numpy import savetxt
from pathlib import Path

from phys2bids.cli.split import _get_parser
from phys2bids.physio_obj import BlueprintInput

LGR = logging.getLogger(__name__)

def split2phys(filename, indir='.', outdir='.', ntp_list=[0], tr_list=[1], thr=None):
    """
    Parallel workflow of phys2bids
    Runs the split parser, does some check on inputs and calls
    phys2bids to handle each dictionaries that have been created
    based on npt_list and tr_list
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
    LGR.info(f'Currently running phys2bids version {version_number}')
    LGR.info(f'Input file is {filename}')

    # Check options to make them internally coherent pt. II
    # #!# This can probably be done while parsing?
    indir = utils.check_input_dir(indir)
    filename, ftype = utils.check_input_type(filename,
                                             indir)

    infile = os.path.join(indir, filename)
    utils.check_file_exists(infile)

    # Read file!
    if ftype == 'acq':
        from phys2bids.interfaces.acq import populate_phys_input
    elif ftype == 'txt':
        from phys2bids.interfaces.txt import populate_phys_input
    else:
        # #!# We should add a logger here.
        raise NotImplementedError('Currently unsupported file type.')

    # Check equivalence of list_ntp and list_tr
    if list_tr.size[0] = 1:
        list_tr = list_tr * np.ones(list_ntp.size)

    # TODO : sum(ntp_list) is equivalent to num_timepoints_found
    BlueprintInput.check_trigger_amount()

    # TODO : initialize dictionaries for which to call phys2bids()



def _main(argv=None):
    options = _get_parser().parse_args(argv)
    split2phys(**vars(options))


if __name__ == '__main__':
    _main()
