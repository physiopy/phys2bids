# import sys
import fnmatch


def heur(physinfo, name, task='', acq='', direct='', rec='', run=''):
    # ############################## #
    # ##       Modify here!       ## #
    # ##                          ## #
    # ##  Possible variables are: ## #
    # ##    -task (required)      ## #
    # ##    -run                  ## #
    # ##    -rec                  ## #
    # ##    -acq                  ## #
    # ##    -direct               ## #
    # ##                          ## #
    # ##                          ## #
    # ##    See example below     ## #
    # ############################## #

    if physinfo == 'origfilename1':
        task = 'newname1'
    elif physinfo == 'origfilename2':
        task = 'newname2'
        run = 'runnum'
    elif physinfo == 'BH4':
        task = 'breathhold'
    elif fnmatch.fnmatchcase(physinfo, 'MOTOR?'):
        task = 'motor'
    elif fnmatch.fnmatchcase(physinfo, 'LOCALIZER?'):
        task = 'pinel'
    elif fnmatch.fnmatchcase(physinfo, 'SIMON?'):
        task = 'simon'
    elif physinfo == 'RS1':
        task = 'rest'
        run = '01'
    elif physinfo == 'RS2':
        task = 'rest'
        run = '02'
    elif physinfo == 'RS3':
        task = 'rest'
        run = '03'
    elif physinfo == 'RS4':
        task = 'rest'
        run = '04'
        # ############################## #
        # ## Don't modify below this! ## #
        # ############################## #
    else:
        # #!# Transform sys.exit in debug warnings or raiseexceptions!
        # #!# Make all of the above a dictionary
        raise Warning(f'The heuristic {__file__} could not deal with {physinfo}')

    if not task:
        raise KeyError(f'No "task" attribute found')

    name = name + '_task-' + task

    # filename spec: sub-<label>[_ses-<label>]_task-<label>[_acq-<label>] ...
    #                ... [_ce-<label>][_dir-<label>][_rec-<label>] ...
    #                ... [_run-<index>][_recording-<label>]_physio
    if acq:
        name = name + '_acq-' + acq

    if direct:
        name = name + '_dir-' + direct

    if rec:
        name = name + '_rec-' + rec

    if run:
        name = name + '_run-' + run

    return name
