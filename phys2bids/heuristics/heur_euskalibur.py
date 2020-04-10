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

    if physinfo == 'origfilename1':
        info['task'] = 'newname1'
    elif physinfo == 'origfilename2':
        info['task'] = 'newname2'
        info['run'] = 'runnum'
    elif physinfo == 'BH4':
        info['task'] = 'breathhold'
    elif fnmatch.fnmatchcase(physinfo, 'MOTOR?'):
        info['task'] = 'motor'
    elif fnmatch.fnmatchcase(physinfo, 'LOCALIZER?'):
        info['task'] = 'pinel'
    elif fnmatch.fnmatchcase(physinfo, 'SIMON?'):
        info['task'] = 'simon'
    elif physinfo == 'RS1':
        info['task'] = 'rest'
        info['run'] = '01'
    elif physinfo == 'RS2':
        info['task'] = 'rest'
        info['run'] = '02'
    elif physinfo == 'RS3':
        info['task'] = 'rest'
        info['run'] = '03'
    elif physinfo == 'RS4':
        info['task'] = 'rest'
        info['run'] = '04'
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
