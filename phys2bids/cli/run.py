# -*- coding: utf-8 -*-

import argparse

from .. import __version__


def _get_parser():
    """
    Parses command line inputs for this function

    Returns
    -------
    parser.parse_args() : argparse dict

    """
    parser = argparse.ArgumentParser()
    # Argument parser follow template provided by RalphyZ.
    # https://stackoverflow.com/a/43456577
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('Required Argument:')
    required.add_argument('-in', '--input-file',
                          dest='filename',
                          type=str,
                          help=('The name of the acq file, with or without '
                                'extension.   Must be an .acq file!'),
                          required=True)
    optional.add_argument('-info', '--info',
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
                          help=('Folder where output should be placed.'
                                'If \"-heur\" is used, it\'ll become '
                                'the site folder. Requires \"-sub\",'
                                ' and it\'s possible to specify \"-ses\""'),
                          default='.')
    optional.add_argument('-heur', '--heuristic',
                          dest='heur_file',
                          type=str,
                          help=('File containing heuristic, with or without '
                                'extension. Specify path to it if necessary.'),
                          default=None)
    # optional.add_argument('-hdir', '--heur-dir',
    #                       dest='heurdir',
    #                       type=str,
    #                       help='Folder containing heuristic file.',
    #                       default='.')
    optional.add_argument('-sub', '--subject',
                          dest='sub',
                          type=str,
                          help=('To be specified with \"-heur\". Code of '
                                'subject to process.'
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-ses', '--session',
                          dest='ses',
                          type=str,
                          help=('To be specified with \"-heur\". Code of '
                                'session to process.'
                                'Specify path to it if necessary.'),
                          default=None)
    optional.add_argument('-chtrig', '--channel-trigger',
                          dest='chtrig',
                          type=int,
                          help=('The number corresponding to the trigger channel.'
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
                          # #!# Has to go to empty list
                          default=['time', 'respiratory_chest', 'trigger',
                                   'cardiac', 'respiratory_CO2', 'respiratory_O2'])

    optional.add_argument('-v', '--version', action='version',
                          version=('%(prog)s ' + __version__))

    parser._action_groups.append(optional)

    return parser


if __name__ == '__main__':
    raise RuntimeError('phys2bids/cli/run.py should not be run directly;\n'
                       'Please `pip install` phys2bids and use the '
                       '`phys2bids` command')
