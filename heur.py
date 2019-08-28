import sys
import os
import fnmatch.filter as match


def heuristic(filename):
    ################################
    ###       Modify here!       ###
    ###                          ###
    ###  Possible variables are: ###
    ###    -task (required)      ###
    ###    -rec                  ###
    ###    -acq                  ###
    ###    -dir                  ###
    ###                          ###
    ###                          ###
    ###    See example below     ###
    ################################

    if filename == 'origfilename1':
        task = 'newname1'
    elif filename == 'origfilename2':
        task = 'newname2'
        run = 'runnum'
    elif filename == 'BH4':
        task = 'breathhold'
    elif match(filename, 'MOTOR?'):
        task = 'motor'
    elif match(filename, 'PINEL?'):
        task = 'pinel'
    elif match(filename, 'SIMON?'):
        task = 'simon'
    elif filename == 'RS1':
        task = 'rest'
        run = '01'
    elif filename == 'RS2':
        task = 'rest'
        run = '02'
    elif filename == 'RS3':
        task = 'rest'
        run = '03'
    elif filename == 'RS4':
        task = 'rest'
        run = '04'
        ################################
        ### Don't modify below this! ###
        ################################
    else:
        sys.exit()
