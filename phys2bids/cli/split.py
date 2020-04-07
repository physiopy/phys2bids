# -*- coding: utf-8 -*-
"""
Parser for split2phys
"""

import argparse

from phys2bids import __version__


def _get_parser():
    """
    Parses command line inputs for this function

    Returns
    -------
    parser.parse_args() : argparse dict

    Notes
    -----
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    """
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required Argument:')
    required.add_argument('-in', '--input-file',
                          dest='filename',
                          type=str,
                          help='The name of the file containing physiological data, with or '
                               'without extension.',
                          required=True)

    optional.add_argument('-info', '--info',
                          dest='info',
                          action='store_true',
                          help='Only output info about the file, don\'t process. '
                               'Default is to process.',
                          default=False)

    optional.add_argument('-indir', '--input-dir',
                          dest='indir',
                          type=str,
                          help='Folder containing input. '
                               'Default is current folder.',
                          default='.')

    optional.add_argument('-outdir', '--output-dir',
                          dest='outdir',
                          type=str,
                          help='Folder where output should be placed. '
                               'Default is current folder. '
                               'If \"-heur\" is used, it\'ll become '
                               'the site folder. Requires \"-sub\". '
                               'Optional to specify \"-ses\".',
                          default='.')

    required.add_argument('-tr_ls', '--tr_list',
                          dest='tr_list',
                          type=list,
                          help='A list containing the TR(s) of the sequences used in the different '
                               'runs contained in the file',
                          required=True)

    required.add_argument('-ntp_ls', '--numtps_list',
                          dest='ntp_list',
                          type=list,
                          help='A list containing the number of trigger time points in each run',
                          required=True)

    optional.add_argument('-thr', '--threshold',
                          dest='thr',
                          type=float,
                          help='Threshold to use for trigger detection. '
                               'If "ntp" and "TR" are specified, phys2bids automatically computes '
                               'a threshold to detect the triggers. Use this parameter to set it '
                               'manually',
                               default=None)
    optional.add_argument('-v', '--version', action='version',
                          version=('%(prog)s ' + __version__))

    parser._action_groups.append(optional)

    return parser
