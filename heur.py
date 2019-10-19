import sys
import fnmatch

print("""    phys2bids  Copyright (C) 2019  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details add the argument `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; add the argument `show c' for details.""")
if sys.argv[1] == 'show w':
   print(" THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. \nEXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM \n“AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,\n THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. \nTHE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. \nSHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")
if sys.argv[1] == 'show c':
   print("""5. Conveying Modified Source Versions.
You may convey a work based on the Program, or the modifications to produce it from the Program, in the form of source code under the terms of section 4, provided that you also meet all of these conditions:
a) The work must carry prominent notices stating that you modified it, and giving a relevant date.
b) The work must carry prominent notices stating that it is released under this License and any conditions added under section 7. This requirement modifies the requirement in section 4 to “keep intact all notices”.
c) You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy. This License will therefore apply, along with any applicable section 7 additional terms, to the whole of the work, and all its parts, regardless of how they are packaged. This License gives no permission to license the work in any other way, but it does not invalidate such permission if you have separately received it.
d) If the work has interactive user interfaces, each must display Appropriate Legal Notices; however, if the Program has interactive interfaces that do not display Appropriate Legal Notices, your work need not make them do so.
A compilation of a covered work with other separate and independent works, which are not by their nature extensions of the covered work, and which are not combined with it such as to form a larger program, in or on a volume of a storage or distribution medium, is called an “aggregate” if the compilation and its resulting copyright are not used to limit the access or legal rights of the compilation's users beyond what the individual works permit. Inclusion of a covered work in an aggregate does not cause this License to apply to the other parts of the aggregate.""")
VERSION = '0.3.0'
SET_DPI = 100
FIGSIZE = (18, 10)


def heur(physinfo, name, task='', acq='', direct='', rec='', run=''):
    # ############################## #
    # ##       Modify here!       ## #
    # ##                          ## #
    # ##  Possible variables are: ## #
    # ##    -task (required)      ## #
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
        print('File not found in heuristics!\nExiting')
        sys.exit()

    if not task:
        print('No "task" specified for this file!\nExiting')
        sys.exit()

    name = name + '_task-' + task

    # filename spec: sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_recording-<label>]_physio
    if acq:
        name = name + '_acq-' + acq

    if direct:
        name = name + '_dir-' + direct

    if rec:
        name = name + '_rec-' + rec

    if run:
        name = name + '_run-' + run

    return name
