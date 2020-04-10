import fnmatch
import logging

LGR = logging.getLogger(__name__)


def heur(physinfo, info):
    """
    Set of if .. elif statements to fill BIDS names.

    Requires the user (you!) to adjust it accordingly!
    The `if ..` structure should always be similar to
    ```
    if physinfo == 'somepattern':
        info['var'] = 'somethingelse'
    ```
    or, in case it's a partial match
    ```
    if fnmatch.fnmatchcase(physinfo, '*somepattern?'):
        info['var'] = 'somethingelse'
    ```

    Where:
        - `physinfo` and `info` are dedicated keywords,
        - 'somepattern' is the name of the file,
        - 'var' is a bids key in the list below
        - 'somethingelse' is the value of the key

    Parameters
    ----------
    physinfo: str
        Name of the file or partial match
    info: dictionary of str
        Dictionary containing BIDS keys

    Returns
    -------
    info: dictionary of str
        Populated dictionary containing BIDS keys
    """
    # ################################# #
    # ##        Modify here!         ## #
    # ##                             ## #
    # ##  Possible variables are:    ## #
    # ##    -info['task'] (required) ## #
    # ##    -info['run']             ## #
    # ##    -info['rec']             ## #
    # ##    -info['acq']             ## #
    # ##    -info['dir']             ## #
    # ##                             ## #
    # ##  Remember that they are     ## #
    # ##  dictionary keys            ## #
    # ##  See example below          ## #
    # ################################# #

    if fnmatch.fnmatchcase(physinfo, '*tutorial*'):
        info['task'] = 'test'
        info['run'] = '01'
        info['rec'] = 'labchart'
    elif physinfo == 'Example':
        info['task'] = 'rest'
        info['run'] = '01'
        info['acq'] = 'resp'
        # ############################## #
        # ## Don't modify below this! ## #
        # ############################## #
    else:
        # #!# Transform sys.exit in debug warnings or raiseexceptions!
        # #!# Make all of the above a dictionary
        LGR.warning(f'The heuristic {__file__} could not deal with {physinfo}')

    # filename spec: sub-<label>[_ses-<label>]_task-<label>[_acq-<label>] ...
    #                ... [_ce-<label>][_dir-<label>][_rec-<label>] ...
    #                ... [_run-<index>][_recording-<label>]_physio

    return info
