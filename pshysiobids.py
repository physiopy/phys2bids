import os
import argparse

import numpy as np
import matplotlib.pyplot as plt

from bioread import read_file

VERSION=3.0.0

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
    required = parser.add_argument_group('required arguments')
    required.add_argument('-in', '--input-file',
                          dest='filename',
                          type=str,
                          help=('The name of the acq file, with or without ',
                                'extension.   Must be an .acq file!'),
                          required=True)
    optional.add_argument('-indir', '--input-dir',
                          dest='indir',
                          type=str,
                          help='Folder containing input.',
                          default='.')
    optional.add_argument('-outdir', '--output-dir',
                          dest='outdir',
                          type=str,
                          help=('Folder where output should be placed. If \"-heur\" is used, ',
                                'It\'ll become the site folder. Requires \"-sub\",',
                                ' and it\'s possible to specify \"-ses\""'),
                          default='heur.py')
    optional.add_argument('-heur', '--heuristic',
                          dest='heur',
                          type=str,
                          help=('File containing heuristic, with or without extension. ',
                                'Specify path to it if necessary.'),
                          default='.')

    optional.add_argument('-nf', '--newfreq',
                          dest='newfreq',
                          type=float,
                          help='Desired frequency of the biopac files',
                          default=40)
    optional.add_argument('-itr', '--ign_tr',
                          dest='ign_tr',
                          type=float,
                          help='Number of timepoints to discard',
                          default=400)
    optional.add_argument('-itr', '--ign_tr',
                          dest='ign_tr',
                          type=float,
                          help='Number of timepoints to discard',
                          default=400)
    optional.add_argument('-itr', '--ign_tr',
                          dest='ign_tr',
                          type=float,
                          help='Number of timepoints to discard',
                          default=400)
    optional.add_argument('-itr', '--ign_tr',
                          dest='ign_tr',
                          type=float,
                          help='Number of timepoints to discard',
                          default=400)
    parser._action_groups.append(optional)
    return parser